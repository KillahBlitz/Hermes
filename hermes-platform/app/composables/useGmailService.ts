export interface EmailSummary {
  id: string
  thread_id: string
  sender: string
  sender_email: string
  subject: string
  snippet: string
  is_starred: boolean
  is_important: boolean
  date: string
}

export interface EmailAttachment {
  filename: string
  mime_type: string
  size: number
  attachment_id: string
}

export interface EmailDetail {
  id: string
  thread_id: string
  sender: string
  sender_email: string
  recipients: string
  subject: string
  date: string
  body_html?: string
  body_text?: string
  labels: string[]
  attachments: EmailAttachment[]
}

export const useGmailService = () => {
  const config = useRuntimeConfig()
  const { sessionToken } = useAuth()

  const emails = useState<EmailSummary[]>('gmail_emails', () => [])
  const loading = useState<boolean>('gmail_loading', () => false)
  const error = useState<string | null>('gmail_error', () => null)
  const activeFilter = useState<'all' | 'starred' | 'important'>('gmail_filter', () => 'all')
  const searchQuery = useState<string>('gmail_search', () => '')

  // Pagination state (10 per page)
  const pageSize = 10
  const currentPage = useState<number>('gmail_current_page', () => 1)
  const pageTokens = useState<string[]>('gmail_page_tokens', () => [''])
  const nextPageToken = useState<string | null>('gmail_next_token', () => null)

  const hasNextPage = computed(() => !!nextPageToken.value)
  const hasPrevPage = computed(() => currentPage.value > 1)

  const selectedEmail = useState<EmailDetail | null>('gmail_selected_email', () => null)
  const isDetailOpen = useState<boolean>('gmail_detail_open', () => false)
  const detailLoading = useState<boolean>('gmail_detail_loading', () => false)

  const emailToDelete = useState<EmailSummary | EmailDetail | null>('gmail_email_to_delete', () => null)
  const isDeleteModalOpen = useState<boolean>('gmail_delete_modal_open', () => false)
  const isDeleting = useState<boolean>('gmail_is_deleting', () => false)

  const getHeaders = () => ({
    Authorization: `Bearer ${sessionToken.value || ''}`
  })

  const fetchEmails = async (targetPage?: number) => {
    if (!sessionToken.value) return
    
    // Limpiar registros inmediatamente para evitar sensación de congelamiento
    emails.value = []
    loading.value = true
    error.value = null

    const page = targetPage ?? currentPage.value
    currentPage.value = page

    try {
      const apiBaseUrl = config.public.apiBaseUrl
      const tokenForPage = pageTokens.value[page - 1] || ''

      const params = new URLSearchParams({
        filter_type: activeFilter.value,
        max_results: String(pageSize)
      })

      if (searchQuery.value.trim()) {
        params.append('search', searchQuery.value.trim())
      }

      if (tokenForPage) {
        params.append('page_token', tokenForPage)
      }

      const res = await $fetch<{
        emails: EmailSummary[]
        next_page_token?: string
      }>(`${apiBaseUrl}/api/v1/services/emails?${params.toString()}`, {
        headers: getHeaders()
      })

      emails.value = res.emails || []
      nextPageToken.value = res.next_page_token || null

      // Guardar token para la siguiente página si aún no existe en el historial
      if (res.next_page_token && pageTokens.value.length === page) {
        pageTokens.value.push(res.next_page_token)
      }
    } catch (err: any) {
      console.error('Error cargando correos:', err)
      error.value = err.data?.detail || 'No se pudieron cargar los correos de Gmail.'
    } finally {
      loading.value = false
    }
  }

  const setFilter = (filter: 'all' | 'starred' | 'important') => {
    activeFilter.value = filter
    // Limpiar estado y paginación al cambiar de filtro
    currentPage.value = 1
    pageTokens.value = ['']
    nextPageToken.value = null
    emails.value = []
    fetchEmails(1)
  }

  const setSearch = (query: string) => {
    searchQuery.value = query
    // Limpiar estado y paginación al cambiar búsqueda
    currentPage.value = 1
    pageTokens.value = ['']
    nextPageToken.value = null
    emails.value = []
    fetchEmails(1)
  }

  const nextPage = () => {
    if (hasNextPage.value && !loading.value) {
      fetchEmails(currentPage.value + 1)
    }
  }

  const prevPage = () => {
    if (hasPrevPage.value && !loading.value) {
      fetchEmails(currentPage.value - 1)
    }
  }

  const openEmailDetail = async (emailId: string) => {
    if (!sessionToken.value) return
    detailLoading.value = true
    isDetailOpen.value = true
    selectedEmail.value = null

    try {
      const apiBaseUrl = config.public.apiBaseUrl
      const res = await $fetch<EmailDetail>(`${apiBaseUrl}/api/v1/services/emails/${emailId}`, {
        headers: getHeaders()
      })
      selectedEmail.value = res
    } catch (err: any) {
      console.error('Error cargando detalle del correo:', err)
      error.value = err.data?.detail || 'No se pudo cargar el contenido del correo.'
    } finally {
      detailLoading.value = false
    }
  }

  const closeEmailDetail = () => {
    isDetailOpen.value = false
    selectedEmail.value = null
  }

  const promptDeleteEmail = (email: EmailSummary | EmailDetail) => {
    emailToDelete.value = email
    isDeleteModalOpen.value = true
  }

  const cancelDelete = () => {
    emailToDelete.value = null
    isDeleteModalOpen.value = false
  }

  const executeDeleteEmail = async () => {
    if (!emailToDelete.value || !sessionToken.value) return
    isDeleting.value = true

    try {
      const apiBaseUrl = config.public.apiBaseUrl
      const emailId = emailToDelete.value.id
      await $fetch(`${apiBaseUrl}/api/v1/services/emails/${emailId}`, {
        method: 'DELETE',
        headers: getHeaders()
      })

      // Remove from list
      emails.value = emails.value.filter(e => e.id !== emailId)

      // Close detail if deleting currently open email
      if (selectedEmail.value?.id === emailId) {
        closeEmailDetail()
      }
      cancelDelete()
    } catch (err: any) {
      console.error('Error eliminando correo:', err)
      error.value = err.data?.detail || 'No se pudo eliminar el correo.'
    } finally {
      isDeleting.value = false
    }
  }

  return {
    emails,
    loading,
    error,
    activeFilter,
    searchQuery,
    currentPage,
    hasNextPage,
    hasPrevPage,
    pageSize,
    selectedEmail,
    isDetailOpen,
    detailLoading,
    emailToDelete,
    isDeleteModalOpen,
    isDeleting,
    fetchEmails,
    openEmailDetail,
    closeEmailDetail,
    promptDeleteEmail,
    cancelDelete,
    executeDeleteEmail,
    setFilter,
    setSearch,
    nextPage,
    prevPage
  }
}

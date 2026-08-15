import { ref, computed } from 'vue'
import { useAuth } from '~/composables/useAuth'

export interface WishlistImage {
  drive_file_id: string
  name: string
  mime_type: string
  size: number
  thumbnail_link?: string
  web_view_link?: string
}

export interface WishlistItem {
  id: string
  user_id: string
  name: string
  price: number
  currency: string
  category: string
  priority: 'ALTA' | 'MEDIA' | 'BAJA'
  description?: string
  url?: string
  images: WishlistImage[]
  status: 'PENDING' | 'PURCHASED' | 'ARCHIVED'
  purchased_at?: string
  created_at?: string
  updated_at?: string
}

export interface WishlistStats {
  total_items: number
  pending_items: number
  purchased_items: number
  total_pending_value: number
  total_purchased_value: number
  currency: string
}

export interface TodoSection {
  id: string
  user_id?: string
  name: string
  icon: string
  color: string
  is_default: boolean
  order: number
  pending_count: number
  completed_count: number
  created_at?: string
}

export interface TodoTask {
  id: string
  user_id: string
  section_id?: string
  section?: TodoSection
  title: string
  difficulty_points: 1 | 2 | 3 | 5
  repeat: 'NONE' | 'DAILY' | 'WEEKDAYS' | 'WEEKLY' | 'MONTHLY'
  due_date?: string
  notes?: string
  is_completed: boolean
  completed_at?: string
  created_at?: string
  updated_at?: string
}

export const useLists = () => {
  const { sessionToken } = useAuth()
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBaseUrl

  // Vistas
  const activeToolTab = ref<'wishlist' | 'todo'>('wishlist')

  // Datos Wishlist
  const wishlistItems = ref<WishlistItem[]>([])
  const wishlistStats = ref<WishlistStats>({
    total_items: 0,
    pending_items: 0,
    purchased_items: 0,
    total_pending_value: 0,
    total_purchased_value: 0,
    currency: 'MXN'
  })
  const wishlistFilterStatus = ref<string>('')
  const wishlistFilterCategory = ref<string>('')
  const wishlistFilterPriority = ref<string>('')
  const wishlistSearch = ref<string>('')

  // Datos To-Do
  const todoSections = ref<TodoSection[]>([])
  const todoTasks = ref<TodoTask[]>([])
  const selectedSectionId = ref<string>('')
  const todoSearch = ref<string>('')

  // Estados
  const loading = ref(false)
  const error = ref<string | null>(null)

  const getHeaders = () => {
    return {
      Authorization: `Bearer ${sessionToken.value || ''}`
    }
  }

  // ─────────────────────────────────────────────────────────────
  // WISHLIST MÉTODOS
  // ─────────────────────────────────────────────────────────────

  const fetchWishlist = async () => {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams()
      if (wishlistFilterStatus.value) params.append('status', wishlistFilterStatus.value)
      if (wishlistFilterCategory.value) params.append('category', wishlistFilterCategory.value)
      if (wishlistFilterPriority.value) params.append('priority', wishlistFilterPriority.value)
      if (wishlistSearch.value.trim()) params.append('search', wishlistSearch.value.trim())

      const res = await $fetch<{
        items: WishlistItem[]
        stats: WishlistStats
        total: number
      }>(`${apiBase}/api/v1/lists/wishlist?${params.toString()}`, {
        headers: getHeaders()
      })

      wishlistItems.value = res.items
      wishlistStats.value = res.stats
    } catch (err: any) {
      console.error('[useLists] Error al cargar wishlist:', err)
      error.value = err?.data?.detail || 'No se pudo cargar la lista de deseos.'
    } finally {
      loading.value = false
    }
  }

  const createWishlistItem = async (payload: {
    name: string
    price: number
    currency?: string
    category?: string
    priority: string
    description?: string
    url?: string
    status?: string
  }) => {
    try {
      const created = await $fetch<WishlistItem>(`${apiBase}/api/v1/lists/wishlist`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchWishlist()
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear el deseo')
    }
  }

  const updateWishlistItem = async (id: string, payload: Partial<WishlistItem>) => {
    try {
      const updated = await $fetch<WishlistItem>(`${apiBase}/api/v1/lists/wishlist/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchWishlist()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar el deseo')
    }
  }

  const updateWishlistStatus = async (id: string, status: 'PENDING' | 'PURCHASED' | 'ARCHIVED') => {
    try {
      const updated = await $fetch<WishlistItem>(`${apiBase}/api/v1/lists/wishlist/${id}/status`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: { status }
      })
      await fetchWishlist()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar estado')
    }
  }

  const uploadWishlistPhoto = async (itemId: string, file: File) => {
    try {
      const formData = new FormData()
      formData.append('file', file)

      const updated = await $fetch<WishlistItem>(`${apiBase}/api/v1/lists/wishlist/${itemId}/upload-photo`, {
        method: 'POST',
        headers: getHeaders(),
        body: formData
      })
      await fetchWishlist()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al subir foto a Google Drive')
    }
  }

  const deleteWishlistItem = async (id: string) => {
    try {
      await $fetch(`${apiBase}/api/v1/lists/wishlist/${id}`, {
        method: 'DELETE',
        headers: getHeaders()
      })
      await fetchWishlist()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar el deseo')
    }
  }

  // ─────────────────────────────────────────────────────────────
  // TO-DO SECCIONES & TAREAS MÉTODOS
  // ─────────────────────────────────────────────────────────────

  const fetchTodoSections = async () => {
    try {
      const res = await $fetch<{ sections: TodoSection[]; total: number }>(`${apiBase}/api/v1/lists/todo/sections`, {
        headers: getHeaders()
      })
      todoSections.value = res.sections
      if (!selectedSectionId.value && res.sections.length > 0) {
        selectedSectionId.value = res.sections[0]?.id || ''
      }
    } catch (err: any) {
      console.error('[useLists] Error al cargar secciones:', err)
    }
  }

  const createTodoSection = async (payload: { name: string; icon: string; color: string }) => {
    try {
      const created = await $fetch<TodoSection>(`${apiBase}/api/v1/lists/todo/sections`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchTodoSections()
      selectedSectionId.value = created.id
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear la sección')
    }
  }

  const updateTodoSection = async (id: string, payload: Partial<TodoSection>) => {
    try {
      const updated = await $fetch<TodoSection>(`${apiBase}/api/v1/lists/todo/sections/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchTodoSections()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar sección')
    }
  }

  const deleteTodoSection = async (id: string) => {
    try {
      await $fetch(`${apiBase}/api/v1/lists/todo/sections/${id}`, {
        method: 'DELETE',
        headers: getHeaders()
      })
      if (selectedSectionId.value === id) {
        selectedSectionId.value = ''
      }
      await fetchTodoSections()
      await fetchTodoTasks()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar sección')
    }
  }

  const fetchTodoTasks = async () => {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams()
      if (selectedSectionId.value) params.append('section_id', selectedSectionId.value)
      if (todoSearch.value.trim()) params.append('search', todoSearch.value.trim())

      const res = await $fetch<{
        tasks: TodoTask[]
        total: number
        pending_count: number
        completed_count: number
      }>(`${apiBase}/api/v1/lists/todo/tasks?${params.toString()}`, {
        headers: getHeaders()
      })

      todoTasks.value = res.tasks
    } catch (err: any) {
      console.error('[useLists] Error al cargar tareas To-Do:', err)
      error.value = err?.data?.detail || 'No se pudieron cargar las tareas.'
    } finally {
      loading.value = false
    }
  }

  const createTodoTask = async (payload: {
    title: string
    section_id?: string
    difficulty_points?: number
    repeat?: string
    due_date?: string
    notes?: string
  }) => {
    try {
      const created = await $fetch<TodoTask>(`${apiBase}/api/v1/lists/todo/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: {
          section_id: payload.section_id || selectedSectionId.value || undefined,
          ...payload
        }
      })
      await fetchTodoTasks()
      await fetchTodoSections()
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear la tarea')
    }
  }

  const updateTodoTask = async (id: string, payload: Partial<TodoTask>) => {
    try {
      const updated = await $fetch<TodoTask>(`${apiBase}/api/v1/lists/todo/tasks/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchTodoTasks()
      await fetchTodoSections()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar tarea')
    }
  }

  const toggleTodoTask = async (id: string, isCompleted: boolean) => {
    try {
      // Optimistic update local
      const idx = todoTasks.value.findIndex(t => t.id === id)
      if (idx !== -1 && todoTasks.value[idx]) {
        todoTasks.value[idx].is_completed = isCompleted
      }

      const updated = await $fetch<TodoTask>(`${apiBase}/api/v1/lists/todo/tasks/${id}/toggle`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: { is_completed: isCompleted }
      })
      await fetchTodoSections()
      return updated
    } catch (err: any) {
      await fetchTodoTasks()
      throw new Error(err?.data?.detail || 'Error al cambiar estado')
    }
  }

  const deleteTodoTask = async (id: string) => {
    try {
      await $fetch(`${apiBase}/api/v1/lists/todo/tasks/${id}`, {
        method: 'DELETE',
        headers: getHeaders()
      })
      await fetchTodoTasks()
      await fetchTodoSections()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar tarea')
    }
  }

  // ─────────────────────────────────────────────────────────────
  // NAVEGACIÓN & REFRESH
  // ─────────────────────────────────────────────────────────────

  const setToolTab = async (tab: 'wishlist' | 'todo') => {
    activeToolTab.value = tab
    if (tab === 'wishlist') {
      await fetchWishlist()
    } else {
      await fetchTodoSections()
      await fetchTodoTasks()
    }
  }

  const selectSection = async (sectionId: string) => {
    selectedSectionId.value = sectionId
    await fetchTodoTasks()
  }

  const refreshAll = async () => {
    if (activeToolTab.value === 'wishlist') {
      await fetchWishlist()
    } else {
      await fetchTodoSections()
      await fetchTodoTasks()
    }
  }

  return {
    // Estado
    activeToolTab,
    wishlistItems,
    wishlistStats,
    wishlistFilterStatus,
    wishlistFilterCategory,
    wishlistFilterPriority,
    wishlistSearch,
    todoSections,
    todoTasks,
    selectedSectionId,
    todoSearch,
    loading,
    error,

    // Wishlist Métodos
    fetchWishlist,
    createWishlistItem,
    updateWishlistItem,
    updateWishlistStatus,
    uploadWishlistPhoto,
    deleteWishlistItem,

    // To-Do Métodos
    fetchTodoSections,
    createTodoSection,
    updateTodoSection,
    deleteTodoSection,
    fetchTodoTasks,
    createTodoTask,
    updateTodoTask,
    toggleTodoTask,
    deleteTodoTask,

    // Navegación
    setToolTab,
    selectSection,
    refreshAll
  }
}

export interface DriveFile {
  id: string
  name: string
  mime_type: string
  size?: string
  thumbnail_url?: string
  web_view_link?: string
  created_time?: string
  modified_time?: string
  is_folder: boolean
  icon_link?: string
}

export interface DriveBucket {
  root_id: string
  root_name: string
  multimedia_id: string
  archivos_id: string
  whitelist_id?: string
  folders: DriveFile[]
}

export interface BreadcrumbItem {
  id: string
  name: string
}

export interface PreviewInfo {
  file_id: string
  file_name: string
  mime_type: string
  web_view_link?: string
  web_content_link?: string
  thumbnail_link?: string
  size?: string
}

export const useDriveBucket = () => {
  const config = useRuntimeConfig()
  const { sessionToken } = useAuth()

  const bucket = useState<DriveBucket | null>('drive_bucket', () => null)
  const currentFolderId = useState<string>('drive_current_folder_id', () => '')
  const currentFolderName = useState<string>('drive_current_folder_name', () => 'hermes')
  const breadcrumbs = useState<BreadcrumbItem[]>('drive_breadcrumbs', () => [])
  const files = useState<DriveFile[]>('drive_files', () => [])
  
  const loading = useState<boolean>('drive_loading', () => false)
  const error = useState<string | null>('drive_error', () => null)

  const isUploading = useState<boolean>('drive_is_uploading', () => false)
  const uploadProgress = useState<number>('drive_upload_progress', () => 0)

  const isCreateFolderOpen = useState<boolean>('drive_create_folder_open', () => false)
  const isCreatingFolder = useState<boolean>('drive_is_creating_folder', () => false)

  const fileToPreview = useState<DriveFile | null>('drive_file_to_preview', () => null)
  const previewInfo = useState<PreviewInfo | null>('drive_preview_info', () => null)
  const isPreviewOpen = useState<boolean>('drive_is_preview_open', () => false)
  const previewLoading = useState<boolean>('drive_preview_loading', () => false)

  const fileToDelete = useState<DriveFile | null>('drive_file_to_delete', () => null)
  const isDeleteModalOpen = useState<boolean>('drive_delete_modal_open', () => false)
  const isDeleting = useState<boolean>('drive_is_deleting', () => false)

  const viewMode = useState<'grid' | 'list'>('drive_view_mode', () => 'grid')

  const getHeaders = () => ({
    Authorization: `Bearer ${sessionToken.value || ''}`
  })

  const initBucket = async () => {
    if (!sessionToken.value) return
    loading.value = true
    error.value = null

    try {
      const apiBaseUrl = config.public.apiBaseUrl
      const res = await $fetch<DriveBucket>(`${apiBaseUrl}/api/v1/services/drive/bucket`, {
        headers: getHeaders()
      })
      bucket.value = res
      currentFolderId.value = res.root_id
      currentFolderName.value = res.root_name
      breadcrumbs.value = [{ id: res.root_id, name: 'hermes' }]

      // Load root files
      await loadFolder(res.root_id, 'hermes', false)
    } catch (err: any) {
      console.error('Error inicializando bucket de Drive:', err)
      error.value = err.data?.detail || 'No se pudo inicializar la carpeta Hermes en Google Drive.'
    } finally {
      loading.value = false
    }
  }

  const loadFolder = async (folderId: string, folderName = '', updateBreadcrumb = true) => {
    if (!sessionToken.value) return
    loading.value = true
    error.value = null

    try {
      const apiBaseUrl = config.public.apiBaseUrl
      const res = await $fetch<{
        files: DriveFile[]
        current_folder_id: string
        current_folder_name: string
      }>(`${apiBaseUrl}/api/v1/services/drive/files?folder_id=${folderId}`, {
        headers: getHeaders()
      })

      files.value = res.files
      currentFolderId.value = folderId
      currentFolderName.value = folderName || res.current_folder_name

      if (updateBreadcrumb) {
        const existingIndex = breadcrumbs.value.findIndex(b => b.id === folderId)
        if (existingIndex >= 0) {
          breadcrumbs.value = breadcrumbs.value.slice(0, existingIndex + 1)
        } else {
          breadcrumbs.value.push({ id: folderId, name: folderName || res.current_folder_name })
        }
      }
    } catch (err: any) {
      console.error('Error cargando archivos de Drive:', err)
      error.value = err.data?.detail || 'No se pudieron cargar los archivos de la carpeta.'
    } finally {
      loading.value = false
    }
  }

  const navigateToBreadcrumb = async (index: number) => {
    const target = breadcrumbs.value[index]
    if (!target) return
    await loadFolder(target.id, target.name, true)
  }

  const createFolder = async (name: string) => {
    if (!sessionToken.value || !name.trim()) return
    isCreatingFolder.value = true

    try {
      const apiBaseUrl = config.public.apiBaseUrl
      await $fetch(`${apiBaseUrl}/api/v1/services/drive/folders`, {
        method: 'POST',
        headers: getHeaders(),
        body: {
          name: name.trim(),
          parent_folder_id: currentFolderId.value
        }
      })
      isCreateFolderOpen.value = false
      await loadFolder(currentFolderId.value, currentFolderName.value, false)
    } catch (err: any) {
      console.error('Error creando carpeta:', err)
      error.value = err.data?.detail || 'No se pudo crear la carpeta.'
    } finally {
      isCreatingFolder.value = false
    }
  }

  const uploadFile = async (file: File) => {
    if (!sessionToken.value) return
    isUploading.value = true
    uploadProgress.value = 10

    try {
      const apiBaseUrl = config.public.apiBaseUrl
      const formData = new FormData()
      formData.append('file', file)
      formData.append('folder_id', currentFolderId.value)

      uploadProgress.value = 50
      await $fetch(`${apiBaseUrl}/api/v1/services/drive/upload`, {
        method: 'POST',
        headers: getHeaders(),
        body: formData
      })
      uploadProgress.value = 100
      await loadFolder(currentFolderId.value, currentFolderName.value, false)
    } catch (err: any) {
      console.error('Error subiendo archivo:', err)
      error.value = err.data?.detail || 'Error al subir el archivo a Google Drive.'
    } finally {
      setTimeout(() => {
        isUploading.value = false
        uploadProgress.value = 0
      }, 500)
    }
  }

  const openPreview = async (file: DriveFile) => {
    if (file.is_folder) {
      await loadFolder(file.id, file.name, true)
      return
    }

    fileToPreview.value = file
    isPreviewOpen.value = true
    previewLoading.value = true
    previewInfo.value = null

    try {
      const apiBaseUrl = config.public.apiBaseUrl
      const res = await $fetch<PreviewInfo>(
        `${apiBaseUrl}/api/v1/services/drive/files/${file.id}/preview`,
        { headers: getHeaders() }
      )
      previewInfo.value = res
    } catch (err: any) {
      console.error('Error obteniendo preview de archivo:', err)
    } finally {
      previewLoading.value = false
    }
  }

  const closePreview = () => {
    isPreviewOpen.value = false
    fileToPreview.value = null
    previewInfo.value = null
  }

  const promptDeleteFile = (file: DriveFile) => {
    fileToDelete.value = file
    isDeleteModalOpen.value = true
  }

  const cancelDelete = () => {
    fileToDelete.value = null
    isDeleteModalOpen.value = false
  }

  const executeDeleteFile = async () => {
    if (!fileToDelete.value || !sessionToken.value) return
    isDeleting.value = true

    try {
      const apiBaseUrl = config.public.apiBaseUrl
      const fileId = fileToDelete.value.id
      await $fetch(`${apiBaseUrl}/api/v1/services/drive/files/${fileId}`, {
        method: 'DELETE',
        headers: getHeaders()
      })

      files.value = files.value.filter(f => f.id !== fileId)
      cancelDelete()
    } catch (err: any) {
      console.error('Error eliminando archivo:', err)
      error.value = err.data?.detail || 'No se pudo enviar el archivo a la papelera.'
    } finally {
      isDeleting.value = false
    }
  }

  const extractDriveId = (input?: string): string => {
    if (!input) return ''
    if (!input.includes('/') && !input.includes('?')) return input
    const idParamMatch = input.match(/[?&]id=([a-zA-Z0-9_-]+)/)
    if (idParamMatch && idParamMatch[1]) return idParamMatch[1]
    const dPathMatch = input.match(/\/d\/([a-zA-Z0-9_-]+)/)
    if (dPathMatch && dPathMatch[1]) return dPathMatch[1]
    const filesPathMatch = input.match(/\/files\/([a-zA-Z0-9_-]+)/)
    if (filesPathMatch && filesPathMatch[1]) return filesPathMatch[1]
    return input
  }

  const getDriveFileContentUrl = (fileIdOrUrl?: string): string => {
    if (!fileIdOrUrl) return ''
    const resolvedId = extractDriveId(fileIdOrUrl)
    if (!resolvedId) return ''
    const apiBaseUrl = config.public.apiBaseUrl
    const tokenParam = sessionToken.value ? `?token=${encodeURIComponent(sessionToken.value)}` : ''
    return `${apiBaseUrl}/api/v1/services/drive/files/${resolvedId}/content${tokenParam}`
  }

  return {
    bucket,
    currentFolderId,
    currentFolderName,
    breadcrumbs,
    files,
    loading,
    error,
    isUploading,
    uploadProgress,
    isCreateFolderOpen,
    isCreatingFolder,
    fileToPreview,
    previewInfo,
    isPreviewOpen,
    previewLoading,
    fileToDelete,
    isDeleteModalOpen,
    isDeleting,
    viewMode,
    initBucket,
    loadFolder,
    navigateToBreadcrumb,
    createFolder,
    uploadFile,
    openPreview,
    closePreview,
    promptDeleteFile,
    cancelDelete,
    executeDeleteFile,
    getDriveFileContentUrl
  }
}

import { ref, computed } from 'vue'
import { useAuth } from '~/composables/useAuth'

export interface Epic {
  id: string
  user_id?: string
  name: string
  description?: string
  color: string
  icon: string
  is_default: boolean
  created_at?: string
  task_count?: number
}

export interface Task {
  id: string
  user_id: string
  title: string
  description?: string
  type: 'IMPROVEMENT' | 'URGENT' | 'PENDING' | 'ANALYSIS'
  complexity: 'XS' | 'S' | 'M' | 'L' | 'XL'
  epic_id?: string
  epic?: Epic
  status: 'TODO' | 'IN_PROGRESS' | 'TESTING' | 'DONE'
  location: 'BOARD' | 'BACKLOG'
  order: number
  due_date?: string
  completed_at?: string
  days_since_completion?: number
  created_at?: string
  updated_at?: string
}

export interface KanbanBoard {
  todo: Task[]
  in_progress: Task[]
  testing: Task[]
  done: Task[]
  total_active: number
  archived_count: number
}

export interface HabitDayInfo {
  day_number: number
  status: 'COMPLETED' | 'FAILED' | 'PENDING'
  date?: string
}

export interface Habit {
  id: string
  user_id: string
  title: string
  description?: string
  icon: string
  color: string
  start_date?: string
  days: HabitDayInfo[]
  current_streak: number
  total_completed: number
  completion_percentage: number
  is_consolidated: boolean
  created_at?: string
  updated_at?: string
}

export interface StickyNote {
  id: string
  user_id: string
  title?: string
  content: string
  color: string
  x: number
  y: number
  z_index: number
  rotation: number
  created_at?: string
  updated_at?: string
}

export const useBoards = () => {
  const { sessionToken } = useAuth()
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBaseUrl

  // Vistas
  const activeMainTab = ref<'activities' | 'habits' | 'canvas'>('activities')
  const activeActivityView = ref<'kanban' | 'backlog' | 'archived'>('kanban')

  // Datos
  const epics = ref<Epic[]>([])
  const kanban = ref<KanbanBoard | null>(null)
  const backlogTasks = ref<Task[]>([])
  const archivedTasks = ref<Task[]>([])
  const habits = ref<Habit[]>([])
  const stickyNotes = ref<StickyNote[]>([])

  // Filtros
  const selectedEpicId = ref<string>('')
  const selectedTypeFilter = ref<string>('')
  const searchQuery = ref<string>('')

  // Estados de carga
  const loading = ref(false)
  const error = ref<string | null>(null)

  const getHeaders = () => ({
    'Content-Type': 'application/json',
    Authorization: `Bearer ${sessionToken.value || ''}`
  })

  // ─────────────────────────────────────────────────────────────
  // ÉPICAS
  // ─────────────────────────────────────────────────────────────

  const fetchEpics = async () => {
    try {
      const headers = getHeaders()
      const res = await $fetch<{ epics: Epic[]; total: number }>(`${apiBase}/api/v1/boards/epics`, { headers })
      epics.value = res.epics
    } catch (err: any) {
      console.error('[useBoards] Error al cargar épicas:', err)
    }
  }

  const createEpic = async (payload: { name: string; description?: string; color: string; icon: string }) => {
    try {
      const headers = getHeaders()
      const created = await $fetch<Epic>(`${apiBase}/api/v1/boards/epics`, {
        method: 'POST',
        headers,
        body: payload
      })
      await fetchEpics()
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear épica')
    }
  }

  const updateEpic = async (id: string, payload: Partial<Epic>) => {
    try {
      const headers = getHeaders()
      const updated = await $fetch<Epic>(`${apiBase}/api/v1/boards/epics/${id}`, {
        method: 'PUT',
        headers,
        body: payload
      })
      await fetchEpics()
      await refreshCurrentView()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar épica')
    }
  }

  const deleteEpic = async (id: string) => {
    try {
      const headers = getHeaders()
      await $fetch(`${apiBase}/api/v1/boards/epics/${id}`, {
        method: 'DELETE',
        headers
      })
      await fetchEpics()
      await refreshCurrentView()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar épica')
    }
  }

  // ─────────────────────────────────────────────────────────────
  // TAREAS (KANBAN / BACKLOG / FINALIZADOS)
  // ─────────────────────────────────────────────────────────────

  const buildTaskParams = () => {
    const params = new URLSearchParams()
    if (selectedEpicId.value) params.append('epic_id', selectedEpicId.value)
    if (selectedTypeFilter.value) params.append('type', selectedTypeFilter.value)
    if (searchQuery.value.trim()) params.append('search', searchQuery.value.trim())
    return params.toString()
  }

  const fetchKanban = async () => {
    loading.value = true
    error.value = null
    try {
      const headers = getHeaders()
      const queryStr = buildTaskParams()
      const res = await $fetch<KanbanBoard>(`${apiBase}/api/v1/boards/tasks/kanban?${queryStr}`, { headers })
      kanban.value = res
    } catch (err: any) {
      console.error('[useBoards] Error al cargar tablero Kanban:', err)
      error.value = err?.data?.detail || 'No se pudo cargar el tablero.'
    } finally {
      loading.value = false
    }
  }

  const fetchBacklog = async () => {
    loading.value = true
    error.value = null
    try {
      const headers = getHeaders()
      const queryStr = buildTaskParams()
      const res = await $fetch<{ tasks: Task[]; total: number }>(`${apiBase}/api/v1/boards/tasks/backlog?${queryStr}`, { headers })
      backlogTasks.value = res.tasks
    } catch (err: any) {
      console.error('[useBoards] Error al cargar backlog:', err)
      error.value = err?.data?.detail || 'No se pudo cargar el backlog.'
    } finally {
      loading.value = false
    }
  }

  const fetchArchived = async () => {
    loading.value = true
    error.value = null
    try {
      const headers = getHeaders()
      const queryStr = buildTaskParams()
      const res = await $fetch<{ tasks: Task[]; total: number }>(`${apiBase}/api/v1/boards/tasks/archived?${queryStr}`, { headers })
      archivedTasks.value = res.tasks
    } catch (err: any) {
      console.error('[useBoards] Error al cargar finalizados:', err)
      error.value = err?.data?.detail || 'No se pudieron cargar las tareas finalizadas.'
    } finally {
      loading.value = false
    }
  }

  const createTask = async (payload: {
    title: string
    description?: string
    type: string
    complexity: string
    epic_id?: string
    status?: string
    location?: string
    due_date?: string
  }) => {
    try {
      const headers = getHeaders()
      const created = await $fetch<Task>(`${apiBase}/api/v1/boards/tasks`, {
        method: 'POST',
        headers,
        body: payload
      })
      await refreshCurrentView()
      await fetchEpics()
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear la tarea')
    }
  }

  const updateTask = async (id: string, payload: Partial<Task>) => {
    try {
      const headers = getHeaders()
      const updated = await $fetch<Task>(`${apiBase}/api/v1/boards/tasks/${id}`, {
        method: 'PUT',
        headers,
        body: payload
      })
      await refreshCurrentView()
      await fetchEpics()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar la tarea')
    }
  }

  const updateTaskStatus = async (id: string, newStatus: 'TODO' | 'IN_PROGRESS' | 'TESTING' | 'DONE') => {
    try {
      const headers = getHeaders()
      const updated = await $fetch<Task>(`${apiBase}/api/v1/boards/tasks/${id}/status`, {
        method: 'PATCH',
        headers,
        body: { status: newStatus }
      })
      await fetchKanban()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al mover de columna')
    }
  }

  const updateTaskLocation = async (id: string, newLocation: 'BOARD' | 'BACKLOG') => {
    try {
      const headers = getHeaders()
      const updated = await $fetch<Task>(`${apiBase}/api/v1/boards/tasks/${id}/location`, {
        method: 'PATCH',
        headers,
        body: { location: newLocation }
      })
      await refreshCurrentView()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al mover ubicación')
    }
  }

  const deleteTask = async (id: string) => {
    try {
      const headers = getHeaders()
      await $fetch(`${apiBase}/api/v1/boards/tasks/${id}`, {
        method: 'DELETE',
        headers
      })
      await refreshCurrentView()
      await fetchEpics()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar la tarea')
    }
  }

  // ─────────────────────────────────────────────────────────────
  // HÁBITOS (21 DÍAS)
  // ─────────────────────────────────────────────────────────────

  const fetchHabits = async () => {
    loading.value = true
    error.value = null
    try {
      const headers = getHeaders()
      const res = await $fetch<{ habits: Habit[]; total: number }>(`${apiBase}/api/v1/boards/habits`, { headers })
      habits.value = res.habits
    } catch (err: any) {
      console.error('[useBoards] Error al cargar hábitos:', err)
      error.value = err?.data?.detail || 'No se pudieron cargar los hábitos.'
    } finally {
      loading.value = false
    }
  }

  const createHabit = async (payload: { title: string; description?: string; icon: string; color: string }) => {
    try {
      const headers = getHeaders()
      const created = await $fetch<Habit>(`${apiBase}/api/v1/boards/habits`, {
        method: 'POST',
        headers,
        body: payload
      })
      await fetchHabits()
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear hábito')
    }
  }

  const updateHabit = async (id: string, payload: Partial<Habit>) => {
    try {
      const headers = getHeaders()
      const updated = await $fetch<Habit>(`${apiBase}/api/v1/boards/habits/${id}`, {
        method: 'PUT',
        headers,
        body: payload
      })
      await fetchHabits()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar hábito')
    }
  }

  const checkHabitDay = async (habitId: string, dayNumber: number, newStatus: 'COMPLETED' | 'FAILED' | 'PENDING') => {
    try {
      const headers = getHeaders()
      const updated = await $fetch<Habit>(`${apiBase}/api/v1/boards/habits/${habitId}/check-day`, {
        method: 'PATCH',
        headers,
        body: { day_number: dayNumber, status: newStatus }
      })

      // Actualizar estado local inmediato
      const idx = habits.value.findIndex(h => h.id === habitId)
      if (idx !== -1) {
        habits.value[idx] = updated
      }
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar día de hábito')
    }
  }

  const deleteHabit = async (id: string) => {
    try {
      const headers = getHeaders()
      await $fetch(`${apiBase}/api/v1/boards/habits/${id}`, {
        method: 'DELETE',
        headers
      })
      await fetchHabits()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar hábito')
    }
  }

  // ─────────────────────────────────────────────────────────────
  // PIZARRÓN DE IDEAS (STICKY NOTES)
  // ─────────────────────────────────────────────────────────────

  const fetchNotes = async () => {
    loading.value = true
    error.value = null
    try {
      const headers = getHeaders()
      const res = await $fetch<{ notes: StickyNote[]; total: number }>(`${apiBase}/api/v1/boards/notes`, { headers })
      stickyNotes.value = res.notes
    } catch (err: any) {
      console.error('[useBoards] Error al cargar post-its:', err)
      error.value = err?.data?.detail || 'No se pudieron cargar las notas adhesivas.'
    } finally {
      loading.value = false
    }
  }

  const createNote = async (payload: { title?: string; content: string; color: string; x: number; y: number }) => {
    try {
      const headers = getHeaders()
      const created = await $fetch<StickyNote>(`${apiBase}/api/v1/boards/notes`, {
        method: 'POST',
        headers,
        body: payload
      })
      stickyNotes.value.push(created)
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear nota adhesiva')
    }
  }

  const updateNote = async (id: string, payload: Partial<StickyNote>) => {
    try {
      const headers = getHeaders()
      const updated = await $fetch<StickyNote>(`${apiBase}/api/v1/boards/notes/${id}`, {
        method: 'PUT',
        headers,
        body: payload
      })
      const idx = stickyNotes.value.findIndex(n => n.id === id)
      if (idx !== -1) stickyNotes.value[idx] = updated
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar nota adhesiva')
    }
  }

  const updateNotePosition = async (id: string, x: number, y: number, zIndex?: number) => {
    try {
      const headers = getHeaders()
      const updated = await $fetch<StickyNote>(`${apiBase}/api/v1/boards/notes/${id}/position`, {
        method: 'PATCH',
        headers,
        body: { x, y, z_index: zIndex || 1 }
      })
      const idx = stickyNotes.value.findIndex(n => n.id === id)
      if (idx !== -1) stickyNotes.value[idx] = updated
      return updated
    } catch (err: any) {
      console.error('[useBoards] Error guardando posición:', err)
    }
  }

  const deleteNote = async (id: string) => {
    try {
      const headers = getHeaders()
      await $fetch(`${apiBase}/api/v1/boards/notes/${id}`, {
        method: 'DELETE',
        headers
      })
      stickyNotes.value = stickyNotes.value.filter(n => n.id !== id)
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar nota adhesiva')
    }
  }

  // ─────────────────────────────────────────────────────────────
  // REFRESH & VISTA ACTIVA
  // ─────────────────────────────────────────────────────────────

  const refreshCurrentView = async () => {
    if (activeMainTab.value === 'activities') {
      if (activeActivityView.value === 'kanban') await fetchKanban()
      else if (activeActivityView.value === 'backlog') await fetchBacklog()
      else if (activeActivityView.value === 'archived') await fetchArchived()
    } else if (activeMainTab.value === 'habits') {
      await fetchHabits()
    } else if (activeMainTab.value === 'canvas') {
      await fetchNotes()
    }
  }

  const refreshAll = async () => {
    await fetchEpics()
    await refreshCurrentView()
  }

  const setMainTab = async (tab: 'activities' | 'habits' | 'canvas') => {
    activeMainTab.value = tab
    await refreshCurrentView()
  }

  const setActivityView = async (view: 'kanban' | 'backlog' | 'archived') => {
    activeActivityView.value = view
    await refreshCurrentView()
  }

  const setFilters = async (epicId: string, typeFilter: string, search: string) => {
    selectedEpicId.value = epicId
    selectedTypeFilter.value = typeFilter
    searchQuery.value = search
    await refreshCurrentView()
  }

  return {
    // Estado
    activeMainTab,
    activeActivityView,
    epics,
    kanban,
    backlogTasks,
    archivedTasks,
    habits,
    stickyNotes,
    selectedEpicId,
    selectedTypeFilter,
    searchQuery,
    loading,
    error,

    // Métodos Épicas
    fetchEpics,
    createEpic,
    updateEpic,
    deleteEpic,

    // Métodos Tareas
    fetchKanban,
    fetchBacklog,
    fetchArchived,
    createTask,
    updateTask,
    updateTaskStatus,
    updateTaskLocation,
    deleteTask,

    // Métodos Hábitos
    fetchHabits,
    createHabit,
    updateHabit,
    checkHabitDay,
    deleteHabit,

    // Métodos Notas
    fetchNotes,
    createNote,
    updateNote,
    updateNotePosition,
    deleteNote,

    // Navegación y Filtros
    setMainTab,
    setActivityView,
    setFilters,
    refreshCurrentView,
    refreshAll
  }
}

import { ref, computed } from 'vue'
import { useAuth } from '~/composables/useAuth'

// ─────────────────────────────────────────────────────────────
// INTERFACES: ÁRBOL DE MAPAS (ROADMAPS)
// ─────────────────────────────────────────────────────────────

export interface RoadmapNode {
  id: string
  title: string
  icon: string
  color: string
  status: 'PENDIENTE' | 'EN_CURSO' | 'DOMINADO'
  x: number
  y: number
  description?: string
  note_id?: string
  note_title?: string
}

export interface RoadmapEdge {
  id: string
  source_node_id: string
  target_node_id: string
  label?: string
}

export interface Roadmap {
  id: string
  user_id: string
  title: string
  description?: string
  category: string
  color: string
  nodes: RoadmapNode[]
  edges: RoadmapEdge[]
  created_at?: string
  updated_at?: string
}

// ─────────────────────────────────────────────────────────────
// INTERFACES: GESTOR DE HITOS (MILESTONES)
// ─────────────────────────────────────────────────────────────

export interface MilestoneTopic {
  id: string
  title: string
  is_completed: boolean
  completed_at?: string
}

export interface Milestone {
  id: string
  user_id: string
  title: string
  category: 'TITULACION' | 'CERTIFICACION' | 'EXAMEN' | 'PROYECTO' | 'CARRERA' | string
  icon: string
  color: string
  target_date: string
  description?: string
  topics: MilestoneTopic[]
  total_topics: number
  completed_topics: number
  progress_percentage: number
  days_remaining: number
  is_overdue: boolean
  status: 'IN_PROGRESS' | 'COMPLETED' | 'ARCHIVED'
  created_at?: string
  updated_at?: string
}

// ─────────────────────────────────────────────────────────────
// INTERFACES: BÓVEDA ZETTELKASTEN (NOTES & GRAPH)
// ─────────────────────────────────────────────────────────────

export interface BacklinkItem {
  id: string
  title: string
  slug: string
}

export interface ZettelNote {
  id: string
  user_id: string
  title: string
  slug: string
  content_md: string
  tags: string[]
  outgoing_links: string[]
  backlinks: BacklinkItem[]
  roadmap_node_id?: string
  created_at?: string
  updated_at?: string
}

export interface GraphNode {
  id: string
  title: string
  tags: string[]
  connections_count: number
  group: string
}

export interface GraphEdge {
  source: string
  target: string
}

export interface KnowledgeGraphData {
  nodes: GraphNode[]
  edges: GraphEdge[]
  all_tags: string[]
  total_notes: number
  total_connections: number
}

export const useProgress = () => {
  const { sessionToken } = useAuth()
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBaseUrl

  // Pestaña activa
  const activeToolTab = ref<'roadmaps' | 'milestones' | 'zettelkasten'>('roadmaps')

  // Datos Árbol de Mapas
  const roadmaps = ref<Roadmap[]>([])
  const activeRoadmapId = ref<string>('')
  const activeRoadmap = computed(() => {
    return roadmaps.value.find(r => r.id === activeRoadmapId.value) || roadmaps.value[0] || null
  })

  // Datos Gestor de Hitos
  const milestones = ref<Milestone[]>([])
  const milestonesFilterCategory = ref<string>('')
  const milestonesFilterStatus = ref<string>('')

  // Datos Zettelkasten
  const notes = ref<ZettelNote[]>([])
  const activeNote = ref<ZettelNote | null>(null)
  const notesSearch = ref<string>('')
  const selectedTag = ref<string>('')
  const isGraphView = ref<boolean>(false)
  const graphData = ref<KnowledgeGraphData>({
    nodes: [],
    edges: [],
    all_tags: [],
    total_notes: 0,
    total_connections: 0
  })

  // Estados generales
  const loading = ref(false)
  const error = ref<string | null>(null)

  const getHeaders = () => ({
    Authorization: `Bearer ${sessionToken.value || ''}`
  })

  // ─────────────────────────────────────────────────────────────
  // ROADMAPS MÉTODOS
  // ─────────────────────────────────────────────────────────────

  const fetchRoadmaps = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await $fetch<{ roadmaps: Roadmap[]; total: number }>(`${apiBase}/api/v1/progress/roadmaps`, {
        headers: getHeaders()
      })
      roadmaps.value = res.roadmaps
      if (!activeRoadmapId.value && res.roadmaps.length > 0) {
        activeRoadmapId.value = res.roadmaps[0]?.id || ''
      }
    } catch (err: any) {
      console.error('[useProgress] Error al cargar roadmaps:', err)
      error.value = err?.data?.detail || 'No se pudieron cargar los mapas de ruta.'
    } finally {
      loading.value = false
    }
  }

  const createRoadmap = async (payload: {
    title: string
    description?: string
    category?: string
    color?: string
    nodes?: RoadmapNode[]
    edges?: RoadmapEdge[]
  }) => {
    try {
      const created = await $fetch<Roadmap>(`${apiBase}/api/v1/progress/roadmaps`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchRoadmaps()
      activeRoadmapId.value = created.id
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear el roadmap')
    }
  }

  const updateRoadmap = async (id: string, payload: Partial<Roadmap>) => {
    try {
      const updated = await $fetch<Roadmap>(`${apiBase}/api/v1/progress/roadmaps/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      const idx = roadmaps.value.findIndex(r => r.id === id)
      if (idx !== -1) {
        roadmaps.value[idx] = updated
      }
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar el roadmap')
    }
  }

  const deleteRoadmap = async (id: string) => {
    try {
      await $fetch(`${apiBase}/api/v1/progress/roadmaps/${id}`, {
        method: 'DELETE',
        headers: getHeaders()
      })
      if (activeRoadmapId.value === id) {
        activeRoadmapId.value = ''
      }
      await fetchRoadmaps()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar el roadmap')
    }
  }

  // ─────────────────────────────────────────────────────────────
  // GESTOR DE HITOS MÉTODOS
  // ─────────────────────────────────────────────────────────────

  const fetchMilestones = async () => {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams()
      if (milestonesFilterCategory.value) params.append('category', milestonesFilterCategory.value)
      if (milestonesFilterStatus.value) params.append('status', milestonesFilterStatus.value)

      const res = await $fetch<{
        milestones: Milestone[]
        total: number
        active_count: number
        completed_count: number
      }>(`${apiBase}/api/v1/progress/milestones?${params.toString()}`, {
        headers: getHeaders()
      })

      milestones.value = res.milestones
    } catch (err: any) {
      console.error('[useProgress] Error al cargar hitos:', err)
      error.value = err?.data?.detail || 'No se pudieron cargar los hitos.'
    } finally {
      loading.value = false
    }
  }

  const createMilestone = async (payload: {
    title: string
    category: string
    icon: string
    color: string
    target_date: string
    description?: string
    topics?: MilestoneTopic[]
  }) => {
    try {
      const created = await $fetch<Milestone>(`${apiBase}/api/v1/progress/milestones`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchMilestones()
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear el hito')
    }
  }

  const updateMilestone = async (id: string, payload: Partial<Milestone>) => {
    try {
      const updated = await $fetch<Milestone>(`${apiBase}/api/v1/progress/milestones/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchMilestones()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar el hito')
    }
  }

  const toggleMilestoneTopic = async (milestoneId: string, topicId: string, isCompleted: boolean) => {
    try {
      // Optimistic update
      const mIdx = milestones.value.findIndex(m => m.id === milestoneId)
      if (mIdx !== -1 && milestones.value[mIdx]) {
        const t = milestones.value[mIdx].topics.find(t => t.id === topicId)
        if (t) t.is_completed = isCompleted
      }

      const updated = await $fetch<Milestone>(
        `${apiBase}/api/v1/progress/milestones/${milestoneId}/topics/${topicId}/toggle`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            ...getHeaders()
          },
          body: { is_completed: isCompleted }
        }
      )
      if (mIdx !== -1) {
        milestones.value[mIdx] = updated
      }
      return updated
    } catch (err: any) {
      await fetchMilestones()
      throw new Error(err?.data?.detail || 'Error al cambiar estado del tema')
    }
  }

  const deleteMilestone = async (id: string) => {
    try {
      await $fetch(`${apiBase}/api/v1/progress/milestones/${id}`, {
        method: 'DELETE',
        headers: getHeaders()
      })
      await fetchMilestones()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar el hito')
    }
  }

  // ─────────────────────────────────────────────────────────────
  // BÓVEDA ZETTELKASTEN & GRAFO MÉTODOS
  // ─────────────────────────────────────────────────────────────

  const fetchNotes = async () => {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams()
      if (notesSearch.value.trim()) params.append('search', notesSearch.value.trim())
      if (selectedTag.value.trim()) params.append('tag', selectedTag.value.trim())

      const res = await $fetch<{ notes: ZettelNote[]; total: number }>(
        `${apiBase}/api/v1/progress/notes?${params.toString()}`,
        { headers: getHeaders() }
      )

      notes.value = res.notes
      if (!activeNote.value && res.notes.length > 0) {
        activeNote.value = res.notes[0] || null
      }
    } catch (err: any) {
      console.error('[useProgress] Error al cargar notas:', err)
      error.value = err?.data?.detail || 'No se pudieron cargar las notas Zettelkasten.'
    } finally {
      loading.value = false
    }
  }

  const fetchNote = async (idOrTitle: string) => {
    try {
      const res = await $fetch<ZettelNote>(
        `${apiBase}/api/v1/progress/notes/${encodeURIComponent(idOrTitle)}`,
        { headers: getHeaders() }
      )
      activeNote.value = res
      return res
    } catch (err: any) {
      console.error('[useProgress] Error al obtener nota:', err)
      return null
    }
  }

  const createNote = async (payload: {
    title: string
    content_md: string
    tags?: string[]
    roadmap_node_id?: string
  }) => {
    try {
      const created = await $fetch<ZettelNote>(`${apiBase}/api/v1/progress/notes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchNotes()
      activeNote.value = created
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear la nota')
    }
  }

  const updateNote = async (id: string, payload: Partial<ZettelNote>) => {
    try {
      const updated = await $fetch<ZettelNote>(`${apiBase}/api/v1/progress/notes/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchNotes()
      if (activeNote.value?.id === id) {
        activeNote.value = updated
      }
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar la nota')
    }
  }

  const deleteNote = async (id: string) => {
    try {
      await $fetch(`${apiBase}/api/v1/progress/notes/${id}`, {
        method: 'DELETE',
        headers: getHeaders()
      })
      if (activeNote.value?.id === id) {
        activeNote.value = null
      }
      await fetchNotes()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar la nota')
    }
  }

  const fetchKnowledgeGraph = async () => {
    try {
      const res = await $fetch<KnowledgeGraphData>(`${apiBase}/api/v1/progress/graph`, {
        headers: getHeaders()
      })
      graphData.value = res
    } catch (err: any) {
      console.error('[useProgress] Error al cargar grafo:', err)
    }
  }

  const openWikilink = async (targetTitle: string) => {
    const existing = await fetchNote(targetTitle)
    if (existing) {
      activeNote.value = existing
    } else {
      // Si la nota no existe, crear borrador inicial
      const created = await createNote({
        title: targetTitle,
        content_md: `# ${targetTitle}\n\nNota creada desde enlace bidireccional Zettelkasten.\n\n`
      })
      activeNote.value = created
    }
  }

  // ─────────────────────────────────────────────────────────────
  // NAVEGACIÓN GENERAL
  // ─────────────────────────────────────────────────────────────

  const setToolTab = async (tab: 'roadmaps' | 'milestones' | 'zettelkasten') => {
    activeToolTab.value = tab
    if (tab === 'roadmaps') {
      await fetchRoadmaps()
    } else if (tab === 'milestones') {
      await fetchMilestones()
    } else if (tab === 'zettelkasten') {
      await fetchNotes()
      await fetchKnowledgeGraph()
    }
  }

  const refreshAll = async () => {
    if (activeToolTab.value === 'roadmaps') {
      await fetchRoadmaps()
    } else if (activeToolTab.value === 'milestones') {
      await fetchMilestones()
    } else {
      await fetchNotes()
      await fetchKnowledgeGraph()
    }
  }

  return {
    // Estado general
    activeToolTab,
    loading,
    error,

    // Roadmaps
    roadmaps,
    activeRoadmapId,
    activeRoadmap,
    fetchRoadmaps,
    createRoadmap,
    updateRoadmap,
    deleteRoadmap,

    // Milestones
    milestones,
    milestonesFilterCategory,
    milestonesFilterStatus,
    fetchMilestones,
    createMilestone,
    updateMilestone,
    toggleMilestoneTopic,
    deleteMilestone,

    // Zettelkasten
    notes,
    activeNote,
    notesSearch,
    selectedTag,
    isGraphView,
    graphData,
    fetchNotes,
    fetchNote,
    createNote,
    updateNote,
    deleteNote,
    fetchKnowledgeGraph,
    openWikilink,

    // Navegación
    setToolTab,
    refreshAll
  }
}

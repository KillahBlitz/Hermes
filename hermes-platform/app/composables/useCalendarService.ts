import { ref, computed } from 'vue'
import { useAuth } from '~/composables/useAuth'

export interface CalendarEvent {
  id: string
  summary: string
  description?: string
  location?: string
  start: string
  end: string
  is_all_day: boolean
  html_link?: string
  status: string
  color_id?: string
  attendees: string[]
  created?: string
  updated?: string
}

export const useCalendarService = () => {
  const { sessionToken } = useAuth()
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBaseUrl

  const events = ref<CalendarEvent[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Current viewed month and selected day
  const currentDate = ref(new Date())
  const selectedDate = ref<Date | null>(new Date())
  const viewMode = ref<'month' | 'agenda'>('month')
  const searchQuery = ref('')

  const getHeaders = () => ({
    Authorization: `Bearer ${sessionToken.value || ''}`
  })

  // Format bounds for current month
  const getMonthBounds = (d: Date) => {
    const year = d.getFullYear()
    const month = d.getMonth()
    // Go 7 days back from start of month and 7 days forward from end of month for seamless calendar grid
    const start = new Date(year, month, -6, 0, 0, 0)
    const end = new Date(year, month + 1, 7, 23, 59, 59)
    return {
      timeMin: start.toISOString(),
      timeMax: end.toISOString()
    }
  }

  const fetchEvents = async (customTimeMin?: string, customTimeMax?: string) => {
    loading.value = true
    error.value = null
    try {
      const bounds = getMonthBounds(currentDate.value)
      const tMin = customTimeMin || bounds.timeMin
      const tMax = customTimeMax || bounds.timeMax

      const params = new URLSearchParams({
        time_min: tMin,
        time_max: tMax,
        max_results: '200'
      })
      if (searchQuery.value.trim()) {
        params.append('q', searchQuery.value.trim())
      }

      const res = await $fetch<{ events: CalendarEvent[]; total: number }>(
        `${apiBase}/api/v1/services/calendar/events?${params.toString()}`,
        { headers: getHeaders() }
      )
      events.value = res.events
    } catch (err: any) {
      console.error('[useCalendarService] Error fetching events:', err)
      error.value = err?.data?.detail || 'No se pudieron cargar los eventos de Google Calendar.'
    } finally {
      loading.value = false
    }
  }

  const createEvent = async (payload: {
    summary: string
    description?: string
    location?: string
    start_time: string
    end_time: string
    is_all_day?: boolean
    color_id?: string
    attendees?: string[]
  }) => {
    try {
      const created = await $fetch<CalendarEvent>(`${apiBase}/api/v1/services/calendar/events`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: payload
      })
      await fetchEvents()
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al programar el evento en Google Calendar')
    }
  }

  const updateEvent = async (id: string, payload: Partial<CalendarEvent>) => {
    try {
      const updated = await $fetch<CalendarEvent>(`${apiBase}/api/v1/services/calendar/events/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: {
          summary: payload.summary,
          description: payload.description,
          location: payload.location,
          start_time: payload.start,
          end_time: payload.end,
          is_all_day: payload.is_all_day,
          color_id: payload.color_id,
          attendees: payload.attendees
        }
      })
      await fetchEvents()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar el evento en Google Calendar')
    }
  }

  const deleteEvent = async (id: string) => {
    try {
      await $fetch(`${apiBase}/api/v1/services/calendar/events/${id}`, {
        method: 'DELETE',
        headers: getHeaders()
      })
      events.value = events.value.filter(e => e.id !== id)
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar el evento de Google Calendar')
    }
  }

  const quickAddEvent = async (text: string) => {
    try {
      const created = await $fetch<CalendarEvent>(`${apiBase}/api/v1/services/calendar/quick-add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders()
        },
        body: { text }
      })
      await fetchEvents()
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error en creación rápida con Google Calendar')
    }
  }

  // Navigation
  const prevMonth = async () => {
    currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1)
    await fetchEvents()
  }

  const nextMonth = async () => {
    currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1)
    await fetchEvents()
  }

  const goToToday = async () => {
    currentDate.value = new Date()
    selectedDate.value = new Date()
    await fetchEvents()
  }

  // Events filtered for selected date
  const selectedDayEvents = computed(() => {
    if (!selectedDate.value) return events.value
    const targetStr = selectedDate.value.toISOString().substring(0, 10)
    return events.value.filter(e => {
      const eventStartStr = e.start ? e.start.substring(0, 10) : ''
      return eventStartStr === targetStr
    })
  })

  return {
    events,
    loading,
    error,
    currentDate,
    selectedDate,
    viewMode,
    searchQuery,
    selectedDayEvents,
    fetchEvents,
    createEvent,
    updateEvent,
    deleteEvent,
    quickAddEvent,
    prevMonth,
    nextMonth,
    goToToday
  }
}

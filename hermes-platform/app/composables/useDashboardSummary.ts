import { ref, computed } from 'vue'
import { useFinance } from '~/composables/useFinance'
import { useCalendarService } from '~/composables/useCalendarService'
import { useBoards } from '~/composables/useBoards'
import { useLists } from '~/composables/useLists'
import { useProgress } from '~/composables/useProgress'

export const useDashboardSummary = () => {
  const finance = useFinance()
  const calendar = useCalendarService()
  const boards = useBoards()
  const lists = useLists()
  const progress = useProgress()

  const loading = ref(true)
  const isRefreshing = ref(false)

  const loadAll = async () => {
    loading.value = true
    try {
      await Promise.allSettled([
        finance.fetchAnalytics(),
        finance.fetchCategories(),
        calendar.fetchEvents(),
        boards.fetchKanban(),
        boards.fetchHabits(),
        lists.fetchTodoSections(),
        lists.fetchTodoTasks(),
        lists.fetchWishlist(),
        progress.fetchMilestones(),
        progress.fetchNotes(),
        progress.fetchRoadmaps()
      ])
    } catch (err) {
      console.error('[useDashboardSummary] Error loading dashboard metrics:', err)
    } finally {
      loading.value = false
    }
  }

  const refresh = async () => {
    isRefreshing.value = true
    await loadAll()
    isRefreshing.value = false
  }

  // Next 3 upcoming calendar events
  const upcomingEvents = computed(() => {
    return (calendar.events.value || [])
      .slice(0, 3)
  })

  // Urgent and in-progress tasks
  const inProgressTasks = computed(() => {
    return boards.kanban.value?.in_progress || []
  })

  const urgentTasksCount = computed(() => {
    const b = boards.kanban.value
    if (!b) return 0
    const all = [...(b.todo || []), ...(b.in_progress || []), ...(b.testing || [])]
    return all.filter(t => t.type === 'URGENT').length
  })

  // Best habit streak
  const topHabit = computed(() => {
    const h = boards.habits.value || []
    if (!h.length) return null
    return [...h].sort((a, b) => b.current_streak - a.current_streak)[0]
  })

  // Nearest critical milestone
  const nearestMilestone = computed(() => {
    const ms = progress.milestones.value || []
    if (!ms.length) return null
    const active = ms.filter(m => m.status !== 'COMPLETED')
    if (!active.length) return ms[0]
    return [...active].sort((a, b) => a.days_remaining - b.days_remaining)[0]
  })

  // Pending To-Do items
  const pendingTodos = computed(() => {
    return (lists.todoTasks.value || [])
      .filter(t => !t.is_completed)
      .slice(0, 4)
  })

  return {
    loading,
    isRefreshing,
    finance,
    calendar,
    boards,
    lists,
    progress,
    upcomingEvents,
    inProgressTasks,
    urgentTasksCount,
    topHabit,
    nearestMilestone,
    pendingTodos,
    loadAll,
    refresh
  }
}

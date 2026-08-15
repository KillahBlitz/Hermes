<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCalendarService } from '~/composables/useCalendarService'
import type { CalendarEvent } from '~/composables/useCalendarService'
import CalendarEventCard from '~/components/molecules/CalendarEventCard.vue'
import CalendarEventModal from '~/components/organisms/CalendarEventModal.vue'

const calendar = useCalendarService()

// Modals
const showEventModal = ref(false)
const eventToEdit = ref<CalendarEvent | null>(null)
const defaultModalDate = ref<Date | null>(null)

// Quick add input
const quickAddText = ref('')
const isQuickAdding = ref(false)

// Delete Confirm
const showDeleteConfirm = ref(false)
const eventToDelete = ref<CalendarEvent | null>(null)

// Toast
const toastMessage = ref('')
const toastType = ref<'success' | 'error'>('success')
const toastVisible = ref(false)
const showToast = (msg: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = msg
  toastType.value = type
  toastVisible.value = true
  setTimeout(() => { toastVisible.value = false }, 3500)
}

// ─────────────────────────────────────────────────────────────
// CALENDAR GRID COMPUTATION
// ─────────────────────────────────────────────────────────────

const weekDays = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

const currentMonthLabel = computed(() => {
  const d = calendar.currentDate.value
  const monthName = d.toLocaleDateString('es-ES', { month: 'long' })
  const year = d.getFullYear()
  return `${monthName.charAt(0).toUpperCase() + monthName.slice(1)} ${year}`
})

interface CalendarDayCell {
  date: Date
  dateStr: string
  dayNumber: number
  isCurrentMonth: boolean
  isToday: boolean
  isSelected: boolean
  events: CalendarEvent[]
}

const calendarGridDays = computed(() => {
  const current = calendar.currentDate.value
  const year = current.getFullYear()
  const month = current.getMonth()

  // First day of current month
  const firstDayOfMonth = new Date(year, month, 1)
  // Day of week: 0 is Sun, 1 is Mon... convert to Monday=0
  let startingDayOfWeek = firstDayOfMonth.getDay() - 1
  if (startingDayOfWeek === -1) startingDayOfWeek = 6

  // Total days in current month
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  // Total days in previous month
  const daysInPrevMonth = new Date(year, month, 0).getDate()

  const cells: CalendarDayCell[] = []
  const todayStr = new Date().toISOString().substring(0, 10)
  const selectedStr = calendar.selectedDate.value ? calendar.selectedDate.value.toISOString().substring(0, 10) : ''

  // 1. Previous month trailing days
  for (let i = startingDayOfWeek - 1; i >= 0; i--) {
    const dayNum = daysInPrevMonth - i
    const d = new Date(year, month - 1, dayNum)
    const dStr = d.toISOString().substring(0, 10)
    cells.push({
      date: d,
      dateStr: dStr,
      dayNumber: dayNum,
      isCurrentMonth: false,
      isToday: dStr === todayStr,
      isSelected: dStr === selectedStr,
      events: getEventsForDateStr(dStr)
    })
  }

  // 2. Current month days
  for (let i = 1; i <= daysInMonth; i++) {
    const d = new Date(year, month, i)
    const dStr = d.toISOString().substring(0, 10)
    cells.push({
      date: d,
      dateStr: dStr,
      dayNumber: i,
      isCurrentMonth: true,
      isToday: dStr === todayStr,
      isSelected: dStr === selectedStr,
      events: getEventsForDateStr(dStr)
    })
  }

  // 3. Next month leading days to complete 35 or 42 cells
  const remainingCells = (cells.length <= 35 ? 35 : 42) - cells.length
  for (let i = 1; i <= remainingCells; i++) {
    const d = new Date(year, month + 1, i)
    const dStr = d.toISOString().substring(0, 10)
    cells.push({
      date: d,
      dateStr: dStr,
      dayNumber: i,
      isCurrentMonth: false,
      isToday: dStr === todayStr,
      isSelected: dStr === selectedStr,
      events: getEventsForDateStr(dStr)
    })
  }

  return cells
})

const getEventsForDateStr = (dateStr: string) => {
  return calendar.events.value.filter(e => {
    const s = e.start ? e.start.substring(0, 10) : ''
    return s === dateStr
  })
}

const getEventChipStyle = (colorId?: string) => {
  const map: Record<string, { border: string; bg: string; dot: string }> = {
    '1': { border: 'rgba(121, 134, 203, 0.45)', bg: 'rgba(121, 134, 203, 0.18)', dot: '#7986cb' },
    '2': { border: 'rgba(51, 182, 121, 0.45)', bg: 'rgba(51, 182, 121, 0.18)', dot: '#33b679' },
    '3': { border: 'rgba(142, 36, 170, 0.45)', bg: 'rgba(142, 36, 170, 0.18)', dot: '#8e24aa' },
    '4': { border: 'rgba(230, 124, 115, 0.45)', bg: 'rgba(230, 124, 115, 0.18)', dot: '#e67c73' },
    '5': { border: 'rgba(246, 191, 38, 0.45)', bg: 'rgba(246, 191, 38, 0.18)', dot: '#f6bf26' },
    '6': { border: 'rgba(244, 81, 30, 0.45)', bg: 'rgba(244, 81, 30, 0.18)', dot: '#f4511e' },
    '7': { border: 'rgba(3, 155, 229, 0.45)', bg: 'rgba(3, 155, 229, 0.18)', dot: '#039be5' },
    '10': { border: 'rgba(11, 128, 67, 0.45)', bg: 'rgba(11, 128, 67, 0.18)', dot: '#0b8043' },
    '11': { border: 'rgba(213, 0, 0, 0.45)', bg: 'rgba(213, 0, 0, 0.18)', dot: '#d50000' },
  }
  const defaultColors = { border: 'rgba(0, 229, 255, 0.35)', bg: 'rgba(0, 229, 255, 0.18)', dot: '#00E5FF' }
  const c = map[colorId || ''] || defaultColors
  return {
    borderColor: c.border,
    background: c.bg,
    '--chip-dot-color': c.dot
  }
}

// ─────────────────────────────────────────────────────────────
// ACCIONES
// ─────────────────────────────────────────────────────────────

const selectDay = (day: CalendarDayCell) => {
  calendar.selectedDate.value = day.date
}

const openCreateModal = (date?: Date) => {
  eventToEdit.value = null
  defaultModalDate.value = date || calendar.selectedDate.value || new Date()
  showEventModal.value = true
}

const openEditModal = (event: CalendarEvent) => {
  eventToEdit.value = event
  showEventModal.value = true
}

const handleSaveEvent = async (payload: any) => {
  try {
    if (payload.id) {
      await calendar.updateEvent(payload.id, payload)
      showToast('Evento actualizado en Google Calendar 📅')
    } else {
      await calendar.createEvent(payload)
      showToast('Evento agendado exitosamente en Google Calendar 🚀')
    }
    showEventModal.value = false
  } catch (err: any) {
    showToast(err.message || 'Error al guardar el evento', 'error')
  }
}

const promptDeleteEvent = (event: CalendarEvent) => {
  eventToDelete.value = event
  showDeleteConfirm.value = true
}

const executeDeleteEvent = async () => {
  if (!eventToDelete.value) return
  try {
    await calendar.deleteEvent(eventToDelete.value.id)
    showToast('Evento eliminado de Google Calendar')
  } catch (err: any) {
    showToast(err.message || 'Error al eliminar el evento', 'error')
  } finally {
    showDeleteConfirm.value = false
    eventToDelete.value = null
  }
}

const handleQuickAdd = async () => {
  const text = quickAddText.value.trim()
  if (!text) return
  isQuickAdding.value = true
  try {
    await calendar.quickAddEvent(text)
    showToast('Evento creado con Google Calendar QuickAdd ⚡')
    quickAddText.value = ''
  } catch (err: any) {
    showToast(err.message || 'Error al crear evento rápido', 'error')
  } finally {
    isQuickAdding.value = false
  }
}

onMounted(async () => {
  await calendar.fetchEvents()
})
</script>

<template>
  <div class="calendar-section">
    <!-- Top Calendar Header & Toolbar -->
    <div class="calendar-toolbar glass-panel">
      <!-- Left: Month Navigation -->
      <div class="nav-month-box">
        <div class="month-title-row">
          <span class="calendar-badge-icon">📅</span>
          <h2 class="month-title">{{ currentMonthLabel }}</h2>
        </div>

        <div class="month-nav-buttons">
          <button type="button" class="nav-btn" title="Mes anterior" @click="calendar.prevMonth">
            ‹
          </button>
          <button type="button" class="today-btn" @click="calendar.goToToday">
            Hoy
          </button>
          <button type="button" class="nav-btn" title="Mes siguiente" @click="calendar.nextMonth">
            ›
          </button>
        </div>
      </div>

      <!-- Center: View Switcher -->
      <div class="view-mode-toggle">
        <button
          type="button"
          class="mode-toggle-btn"
          :class="{ 'is-active': calendar.viewMode.value === 'month' }"
          @click="calendar.viewMode.value = 'month'"
        >
          <span>Cuadrícula Mensual</span>
        </button>
        <button
          type="button"
          class="mode-toggle-btn"
          :class="{ 'is-active': calendar.viewMode.value === 'agenda' }"
          @click="calendar.viewMode.value = 'agenda'"
        >
          <span>Agenda</span>
        </button>
      </div>

      <!-- Right: Action Button -->
      <div class="toolbar-right">
        <button
          type="button"
          class="create-event-btn btn-neon-teal"
          @click="openCreateModal()"
        >
          <span>＋ Agendar Evento</span>
        </button>
      </div>
    </div>

    <!-- Quick Add Natural Language Bar -->
    <div class="quick-add-bar glass-panel">
      <span class="quick-icon">⚡</span>
      <input
        v-model="quickAddText"
        type="text"
        class="quick-input"
        placeholder="Creación rápida con lenguaje natural (ej. 'Reunión de equipo mañana a las 4pm')..."
        :disabled="isQuickAdding"
        @keydown.enter.prevent="handleQuickAdd"
      >
      <button
        type="button"
        class="quick-add-submit-btn btn-neon-blue"
        :disabled="!quickAddText.trim() || isQuickAdding"
        @click="handleQuickAdd"
      >
        <span>{{ isQuickAdding ? 'Creando...' : 'Crear Rápido' }}</span>
      </button>
    </div>

    <!-- MAIN BODY: MONTH GRID OR AGENDA -->
    <div class="calendar-workspace">
      <!-- 1. MONTH VIEW -->
      <div v-if="calendar.viewMode.value === 'month'" class="month-view-layout">
        <!-- Calendar Grid -->
        <div class="month-grid-container glass-panel">
          <!-- Weekdays Header -->
          <div class="weekdays-row">
            <div v-for="wd in weekDays" :key="wd" class="weekday-cell">
              {{ wd }}
            </div>
          </div>

          <!-- Days Cells -->
          <div class="days-grid">
            <div
              v-for="(day, idx) in calendarGridDays"
              :key="idx"
              class="day-cell"
              :class="{
                'not-current-month': !day.isCurrentMonth,
                'is-today': day.isToday,
                'is-selected': day.isSelected
              }"
              @click="selectDay(day)"
              @dblclick="openCreateModal(day.date)"
            >
              <div class="day-cell-top">
                <span class="day-number">{{ day.dayNumber }}</span>
                <span v-if="day.isToday" class="today-dot" title="Hoy" />
              </div>

              <!-- Event Chips Preview -->
              <div class="day-events-preview">
                <div
                  v-for="ev in day.events.slice(0, 2)"
                  :key="ev.id"
                  class="mini-event-chip"
                  :style="getEventChipStyle(ev.color_id)"
                  :title="ev.summary"
                  @click.stop="openEditModal(ev)"
                >
                  <span class="chip-dot" />
                  <span class="chip-title">{{ ev.summary }}</span>
                </div>
                <span v-if="day.events.length > 2" class="more-events-badge">
                  +{{ day.events.length - 2 }} más
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Selected Day Events Drawer -->
        <div class="day-detail-drawer glass-panel">
          <div class="drawer-header">
            <div class="drawer-date-box">
              <span class="drawer-subtitle">Eventos del día</span>
              <h3 class="drawer-date-title">
                {{ calendar.selectedDate.value ? calendar.selectedDate.value.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long' }) : 'Selecciona un día' }}
              </h3>
            </div>
            <button
              type="button"
              class="mini-add-btn"
              title="Agregar evento en este día"
              @click="openCreateModal(calendar.selectedDate.value || undefined)"
            >
              ＋
            </button>
          </div>

          <div v-if="calendar.selectedDayEvents.value.length === 0" class="drawer-empty">
            <span class="empty-icon">☕</span>
            <p class="empty-title">Sin eventos programados</p>
            <p class="empty-desc">No hay compromisos agendados para esta fecha en Google Calendar.</p>
            <button
              type="button"
              class="btn-neon-teal add-day-btn"
              @click="openCreateModal(calendar.selectedDate.value || undefined)"
            >
              ＋ Programar Evento
            </button>
          </div>

          <div v-else class="drawer-events-list">
            <CalendarEventCard
              v-for="ev in calendar.selectedDayEvents.value"
              :key="ev.id"
              :event="ev"
              @edit="openEditModal"
              @delete="promptDeleteEvent"
            />
          </div>
        </div>
      </div>

      <!-- 2. AGENDA VIEW -->
      <div v-else class="agenda-view-layout glass-panel">
        <div class="agenda-header">
          <h3 class="agenda-title">Lista Cronológica de Eventos</h3>
          <span class="agenda-count">{{ calendar.events.value.length }} eventos este mes</span>
        </div>

        <div v-if="calendar.events.value.length === 0" class="agenda-empty">
          <span class="empty-icon">📅</span>
          <p>No se encontraron eventos en este periodo de Google Calendar.</p>
        </div>

        <div v-else class="agenda-grid">
          <CalendarEventCard
            v-for="ev in calendar.events.value"
            :key="ev.id"
            :event="ev"
            @edit="openEditModal"
            @delete="promptDeleteEvent"
          />
        </div>
      </div>
    </div>

    <!-- Modales -->
    <CalendarEventModal
      :show="showEventModal"
      :event-to-edit="eventToEdit"
      :default-date="defaultModalDate"
      @close="showEventModal = false"
      @save="handleSaveEvent"
    />

    <!-- Delete Confirm Modal -->
    <div v-if="showDeleteConfirm" class="modal-backdrop" @click.self="showDeleteConfirm = false">
      <div class="modal-card glass-panel delete-modal">
        <h3 class="delete-title">¿Eliminar evento de Google Calendar?</h3>
        <p class="delete-desc">
          Estás a punto de eliminar <strong>"{{ eventToDelete?.summary }}"</strong>. Este cambio se sincronizará inmediatamente en tu cuenta de Google.
        </p>
        <div class="delete-actions">
          <button type="button" class="btn-cancel" @click="showDeleteConfirm = false">Cancelar</button>
          <button type="button" class="btn-delete" @click="executeDeleteEvent">Sí, Eliminar</button>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <Transition name="toast">
      <div
        v-if="toastVisible"
        class="toast-notification"
        :class="toastType === 'error' ? 'toast-error' : 'toast-success'"
      >
        {{ toastMessage }}
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.calendar-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.calendar-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  border-radius: 14px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
  flex-wrap: wrap;
  gap: 12px;
}

.nav-month-box {
  display: flex;
  align-items: center;
  gap: 16px;
}

.month-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.calendar-badge-icon {
  font-size: 1.2rem;
}

.month-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--hermes-text-primary);
}

.month-nav-buttons {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
}

.nav-btn {
  background: none;
  border: none;
  color: var(--hermes-text-muted);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-primary);
}

.today-btn {
  background: none;
  border: none;
  color: var(--hermes-text-primary);
  font-size: 0.78rem;
  font-weight: 700;
  padding: 0 10px;
  cursor: pointer;
  border-left: 1px solid rgba(255, 255, 255, 0.06);
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  height: 32px;
}

.today-btn:hover {
  color: var(--hermes-accent-teal, #00FFC6);
}

.view-mode-toggle {
  display: flex;
  background: rgba(0, 0, 0, 0.3);
  padding: 3px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.mode-toggle-btn {
  background: none;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--hermes-text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.mode-toggle-btn.is-active {
  background: rgba(0, 229, 255, 0.18);
  color: var(--hermes-accent-blue, #00E5FF);
}

.quick-add-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  border-radius: 12px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.quick-icon {
  font-size: 1.2rem;
  color: var(--hermes-accent-blue, #00E5FF);
}

.quick-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: var(--hermes-text-primary);
  font-size: 0.88rem;
}

.quick-add-submit-btn {
  padding: 6px 14px;
  font-size: 0.8rem;
  border-radius: 8px;
  cursor: pointer;
}

.calendar-workspace {
  display: flex;
  flex-direction: column;
}

.month-view-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 16px;
}

@media (max-width: 1000px) {
  .month-view-layout {
    grid-template-columns: 1fr;
  }
}

.month-grid-container {
  display: flex;
  flex-direction: column;
  padding: 16px;
  border-radius: 14px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.weekdays-row {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.weekday-cell {
  text-align: center;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--hermes-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  min-width: 0;
  overflow: hidden;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  grid-auto-rows: 92px;
  gap: 5px;
  margin-top: 8px;
}

.day-cell {
  height: 92px;
  max-height: 92px;
  min-width: 0;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  padding: 6px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  cursor: pointer;
  transition: all 0.15s ease;
  overflow: hidden;
  box-sizing: border-box;
}

.day-cell:hover {
  background: rgba(0, 229, 255, 0.08);
  border-color: rgba(0, 229, 255, 0.25);
}

.day-cell.not-current-month {
  opacity: 0.35;
}

.day-cell.is-today {
  border-color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.06);
}

.day-cell.is-selected {
  border-color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
}

.day-cell-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-width: 0;
}

.day-number {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
}

.today-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 0 6px var(--hermes-accent-teal, #00FFC6);
  flex-shrink: 0;
}

.day-events-preview {
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow: hidden;
  min-width: 0;
  flex: 1;
}

.mini-event-chip {
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(0, 229, 255, 0.15);
  border: 1px solid rgba(0, 229, 255, 0.3);
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 0.66rem;
  font-weight: 600;
  color: var(--hermes-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}

.mini-event-chip:hover {
  background: rgba(0, 229, 255, 0.3);
}

.chip-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--chip-dot-color, var(--hermes-accent-blue, #00E5FF));
  flex-shrink: 0;
}

.chip-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
  flex: 1;
}

.more-events-badge {
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--hermes-accent-pink, #FF007F);
  margin-top: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Day Detail Drawer */
.day-detail-drawer {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 18px;
  border-radius: 14px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.drawer-subtitle {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--hermes-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.drawer-date-title {
  margin: 2px 0 0 0;
  font-size: 1rem;
  font-weight: 800;
  color: var(--hermes-text-primary);
  text-transform: capitalize;
}

.mini-add-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: rgba(0, 255, 198, 0.15);
  border: 1px solid var(--hermes-accent-teal, #00FFC6);
  color: var(--hermes-accent-teal, #00FFC6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mini-add-btn:hover {
  background: rgba(0, 255, 198, 0.3);
  box-shadow: 0 0 10px rgba(0, 255, 198, 0.4);
}

.drawer-events-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 520px;
  overflow-y: auto;
}

.drawer-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
  text-align: center;
  gap: 8px;
}

.empty-icon {
  font-size: 2.2rem;
}

.empty-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
}

.empty-desc {
  margin: 0;
  font-size: 0.8rem;
  color: var(--hermes-text-muted);
  line-height: 1.4;
}

.add-day-btn {
  margin-top: 8px;
  padding: 6px 14px;
  font-size: 0.8rem;
  border-radius: 6px;
  cursor: pointer;
}

/* Agenda View */
.agenda-view-layout {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  border-radius: 14px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.agenda-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.agenda-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
}

.agenda-count {
  font-size: 0.8rem;
  color: var(--hermes-accent-teal, #00FFC6);
  font-weight: 600;
}

.agenda-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 14px;
}

.agenda-empty {
  text-align: center;
  padding: 50px 20px;
  color: var(--hermes-text-muted);
  font-size: 0.9rem;
}

/* Delete Prompt Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1200;
  padding: 16px;
}

.delete-modal {
  width: 100%;
  max-width: 440px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 77, 77, 0.3);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.delete-title {
  margin: 0;
  font-size: 1.15rem;
  color: var(--hermes-text-primary);
}

.delete-desc {
  margin: 0;
  font-size: 0.85rem;
  color: var(--hermes-text-muted);
  line-height: 1.4;
}

.delete-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.btn-cancel {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted);
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-delete {
  padding: 8px 16px;
  background: rgba(255, 77, 77, 0.2);
  border: 1px solid rgba(255, 77, 77, 0.5);
  color: #ff4d4d;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
}

.btn-delete:hover {
  background: rgba(255, 77, 77, 0.35);
}

/* Toast */
.toast-notification {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1300;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 0.88rem;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.toast-success {
  background: rgba(0, 255, 198, 0.15);
  border: 1px solid var(--hermes-accent-teal, #00FFC6);
  color: var(--hermes-accent-teal, #00FFC6);
}

.toast-error {
  background: rgba(255, 77, 77, 0.15);
  border: 1px solid #ff4d4d;
  color: #ff4d4d;
}
</style>

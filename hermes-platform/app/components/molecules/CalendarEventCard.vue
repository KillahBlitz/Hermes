<script setup lang="ts">
import { computed } from 'vue'
import type { CalendarEvent } from '~/composables/useCalendarService'

const props = defineProps<{
  event: CalendarEvent
}>()

const emit = defineEmits<{
  (e: 'edit', event: CalendarEvent): void
  (e: 'delete', event: CalendarEvent): void
}>()

const timeLabel = computed(() => {
  if (props.event.is_all_day) {
    return 'Todo el día'
  }
  if (!props.event.start) return ''
  try {
    const s = new Date(props.event.start)
    const e = props.event.end ? new Date(props.event.end) : null
    const startTimeStr = s.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
    if (e) {
      const endTimeStr = e.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
      return `${startTimeStr} - ${endTimeStr}`
    }
    return startTimeStr
  } catch {
    return props.event.start
  }
})

const dateLabel = computed(() => {
  if (!props.event.start) return ''
  try {
    const d = new Date(props.event.start)
    return d.toLocaleDateString('es-ES', {
      weekday: 'short',
      day: 'numeric',
      month: 'short'
    })
  } catch {
    return props.event.start
  }
})

const accentColor = computed(() => {
  const map: Record<string, string> = {
    '1': '#7986cb', // Lavender
    '2': '#33b679', // Sage
    '3': '#8e24aa', // Grape
    '4': '#e67c73', // Flamingo
    '5': '#f6bf26', // Banana
    '6': '#f4511e', // Tangerine
    '7': '#039be5', // Peacock
    '8': '#616161', // Graphite
    '9': '#3f51b5', // Blueberry
    '10': '#0b8043', // Basil
    '11': '#d50000', // Tomato
  }
  return map[props.event.color_id || ''] || 'var(--hermes-accent-teal, #00FFC6)'
})
</script>

<template>
  <div
    class="calendar-event-card glass-panel"
    :style="{ '--event-accent': accentColor }"
  >
    <div class="card-left-strip" />

    <div class="card-content">
      <!-- Top Row: Time & Date Badge -->
      <div class="card-top-row">
        <div class="time-badge">
          <span class="time-dot" />
          <span class="time-text">{{ timeLabel }}</span>
        </div>
        <span class="date-badge">{{ dateLabel }}</span>
      </div>

      <!-- Main: Title & Description -->
      <div class="card-body">
        <h4 class="event-title">{{ event.summary }}</h4>
        <p v-if="event.description" class="event-desc">{{ event.description }}</p>
      </div>

      <!-- Location if available -->
      <div v-if="event.location" class="location-row">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
          <circle cx="12" cy="10" r="3" />
        </svg>
        <span class="location-text">{{ event.location }}</span>
      </div>

      <!-- Footer: Link & Actions -->
      <div class="card-footer">
        <a
          v-if="event.html_link"
          :href="event.html_link"
          target="_blank"
          rel="noopener noreferrer"
          class="calendar-link"
          title="Ver en Google Calendar"
        >
          <span>Abrir en Calendar</span>
          <span class="link-arrow">↗</span>
        </a>

        <div class="actions-right">
          <button
            type="button"
            class="action-btn edit-btn"
            title="Editar evento"
            @click="emit('edit', event)"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
            </svg>
          </button>
          <button
            type="button"
            class="action-btn delete-btn"
            title="Eliminar evento"
            @click="emit('delete', event)"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6" />
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.calendar-event-card {
  position: relative;
  display: flex;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.calendar-event-card:hover {
  border-color: rgba(0, 229, 255, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
}

.card-left-strip {
  width: 4px;
  background: var(--event-accent, #00FFC6);
  flex-shrink: 0;
  box-shadow: 0 0 8px var(--event-accent, #00FFC6);
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px 14px;
}

.card-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.time-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--hermes-accent-blue, #00E5FF);
}

.time-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--event-accent, #00FFC6);
}

.date-badge {
  font-size: 0.72rem;
  color: var(--hermes-text-muted);
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  text-transform: capitalize;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.event-title {
  margin: 0;
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
  line-height: 1.3;
}

.event-desc {
  margin: 0;
  font-size: 0.78rem;
  color: var(--hermes-text-muted);
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.location-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: var(--hermes-text-muted);
}

.location-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.calendar-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--hermes-text-muted);
  text-decoration: none;
  transition: color 0.15s ease;
}

.calendar-link:hover {
  color: var(--hermes-accent-blue, #00E5FF);
}

.link-arrow {
  color: var(--hermes-accent-pink, #FF007F);
  font-weight: 800;
}

.actions-right {
  display: flex;
  align-items: center;
  gap: 6px;
}

.action-btn {
  width: 26px;
  height: 26px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.edit-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted);
}

.edit-btn:hover {
  background: rgba(0, 229, 255, 0.15);
  color: var(--hermes-accent-blue, #00E5FF);
  border-color: rgba(0, 229, 255, 0.3);
}

.delete-btn {
  background: rgba(255, 77, 77, 0.08);
  border: 1px solid rgba(255, 77, 77, 0.2);
  color: #ff4d4d;
}

.delete-btn:hover {
  background: rgba(255, 77, 77, 0.25);
  border-color: #ff4d4d;
}
</style>

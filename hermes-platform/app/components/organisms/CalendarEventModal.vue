<script setup lang="ts">
import { ref, watch } from 'vue'
import type { CalendarEvent } from '~/composables/useCalendarService'

const props = defineProps<{
  show: boolean
  eventToEdit?: CalendarEvent | null
  defaultDate?: Date | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: {
    id?: string
    summary: string
    description?: string
    location?: string
    start_time: string
    end_time: string
    is_all_day: boolean
    color_id?: string
  }): void
}>()

const summary = ref('')
const isAllDay = ref(false)
const startDate = ref('')
const startTime = ref('10:00')
const endDate = ref('')
const endTime = ref('11:00')
const location = ref('')
const description = ref('')
const colorId = ref<string>('7') // Default Peacock blue

const colorOptions = [
  { id: '1', color: '#7986cb', label: 'Lavanda' },
  { id: '2', color: '#33b679', label: 'Verde Sabio' },
  { id: '3', color: '#8e24aa', label: 'Uva' },
  { id: '4', color: '#e67c73', label: 'Flamenco' },
  { id: '5', color: '#f6bf26', label: 'Plátano' },
  { id: '6', color: '#f4511e', label: 'Mandarina' },
  { id: '7', color: '#039be5', label: 'Pavo Real (Azul)' },
  { id: '10', color: '#0b8043', label: 'Albahaca' },
  { id: '11', color: '#d50000', label: 'Tomate' }
]

const formatISODate = (d: Date) => d.toISOString().substring(0, 10)

watch(() => props.show, (isOpen) => {
  if (isOpen) {
    if (props.eventToEdit) {
      summary.value = props.eventToEdit.summary
      isAllDay.value = props.eventToEdit.is_all_day
      location.value = props.eventToEdit.location || ''
      description.value = props.eventToEdit.description || ''
      colorId.value = props.eventToEdit.color_id || '7'

      if (props.eventToEdit.start) {
        startDate.value = props.eventToEdit.start.substring(0, 10)
        if (props.eventToEdit.start.includes('T')) {
          startTime.value = props.eventToEdit.start.substring(11, 16)
        }
      }
      if (props.eventToEdit.end) {
        endDate.value = props.eventToEdit.end.substring(0, 10)
        if (props.eventToEdit.end.includes('T')) {
          endTime.value = props.eventToEdit.end.substring(11, 16)
        }
      }
    } else {
      const baseDate = props.defaultDate || new Date()
      summary.value = ''
      isAllDay.value = false
      startDate.value = formatISODate(baseDate)
      endDate.value = formatISODate(baseDate)
      startTime.value = '10:00'
      endTime.value = '11:00'
      location.value = ''
      description.value = ''
      colorId.value = '7'
    }
  }
})

const handleSave = () => {
  if (!summary.value.trim() || !startDate.value) return

  let startVal = ''
  let endVal = ''

  if (isAllDay.value) {
    startVal = startDate.value
    endVal = endDate.value || startDate.value
  } else {
    startVal = `${startDate.value}T${startTime.value}:00`
    endVal = `${endDate.value || startDate.value}T${endTime.value}:00`
  }

  emit('save', {
    id: props.eventToEdit?.id,
    summary: summary.value.trim(),
    description: description.value.trim() || undefined,
    location: location.value.trim() || undefined,
    start_time: startVal,
    end_time: endVal,
    is_all_day: isAllDay.value,
    color_id: colorId.value
  })
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <div class="modal-header">
        <h3 class="modal-title">
          {{ eventToEdit ? 'Editar Evento de Google Calendar' : 'Programar Nuevo Evento' }}
        </h3>
        <button type="button" class="close-btn" @click="emit('close')">✕</button>
      </div>

      <form class="modal-form" @submit.prevent="handleSave">
        <!-- Event Summary / Title -->
        <div class="form-group">
          <label class="form-label">Título del Evento *</label>
          <input
            v-model="summary"
            type="text"
            class="form-input"
            placeholder="ej. Reunión de Arquitectura con Cliente"
            required
          >
        </div>

        <!-- All day toggle -->
        <div class="form-toggle-row">
          <label class="toggle-label">
            <input v-model="isAllDay" type="checkbox" class="toggle-checkbox">
            <span class="toggle-text">Todo el día</span>
          </label>
        </div>

        <!-- Dates & Times -->
        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Fecha de Inicio *</label>
            <input v-model="startDate" type="date" class="form-input" required>
          </div>
          <div v-if="!isAllDay" class="form-group flex-1">
            <label class="form-label">Hora Inicio *</label>
            <input v-model="startTime" type="time" class="form-input" required>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Fecha de Fin *</label>
            <input v-model="endDate" type="date" class="form-input" required>
          </div>
          <div v-if="!isAllDay" class="form-group flex-1">
            <label class="form-label">Hora Fin *</label>
            <input v-model="endTime" type="time" class="form-input" required>
          </div>
        </div>

        <!-- Location -->
        <div class="form-group">
          <label class="form-label">Ubicación o Enlace Virtual</label>
          <input
            v-model="location"
            type="text"
            class="form-input"
            placeholder="ej. Google Meet / Sala de Juntas 3"
          >
        </div>

        <!-- Color Accent -->
        <div class="form-group">
          <label class="form-label">Color de Categoría en Calendar</label>
          <div class="color-picker-row">
            <button
              v-for="c in colorOptions"
              :key="c.id"
              type="button"
              class="color-btn"
              :class="{ 'is-selected': colorId === c.id }"
              :style="{ backgroundColor: c.color }"
              :title="c.label"
              @click="colorId = c.id"
            />
          </div>
        </div>

        <!-- Description -->
        <div class="form-group">
          <label class="form-label">Descripción / Notas</label>
          <textarea
            v-model="description"
            class="form-textarea"
            placeholder="Puntos a tratar, orden del día o notas..."
            rows="2"
          />
        </div>

        <!-- Actions -->
        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="emit('close')">Cancelar</button>
          <button type="submit" class="btn-neon-teal">
            {{ eventToEdit ? 'Guardar Cambios' : 'Agendar Evento' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  padding: 16px;
}

.modal-card {
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.modal-title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted);
  font-size: 1.2rem;
  cursor: pointer;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-row {
  display: flex;
  gap: 12px;
}

.flex-1 {
  flex: 1;
}

.form-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--hermes-text-muted);
}

.form-input,
.form-textarea {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 9px 12px;
  color: var(--hermes-text-primary);
  font-size: 0.85rem;
  outline: none;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  border-color: rgba(0, 229, 255, 0.4);
}

.form-toggle-row {
  display: flex;
  align-items: center;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.toggle-checkbox {
  width: 16px;
  height: 16px;
  accent-color: var(--hermes-accent-teal, #00FFC6);
  cursor: pointer;
}

.toggle-text {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--hermes-text-primary);
}

.color-picker-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.color-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.color-btn.is-selected {
  transform: scale(1.2);
  border-color: #fff;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.4);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-cancel {
  padding: 8px 18px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: var(--hermes-text-muted);
  border-radius: 8px;
  font-size: 0.84rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.12);
  color: var(--hermes-text-primary);
}
</style>

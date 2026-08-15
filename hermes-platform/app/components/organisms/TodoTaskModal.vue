<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { TodoSection, TodoTask } from '~/composables/useLists'

const props = defineProps<{
  show: boolean
  sections: TodoSection[]
  taskToEdit?: TodoTask | null
  defaultSectionId?: string
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: {
    id?: string
    title: string
    section_id?: string
    difficulty_points: number
    repeat: string
    due_date?: string
    notes?: string
    is_completed?: boolean
  }): void
}>()

const formTitle = ref('')
const formSectionId = ref('')
const formDifficulty = ref<1 | 2 | 3 | 5>(1)
const formRepeat = ref('NONE')
const formDueDate = ref('')
const formNotes = ref('')
const formIsCompleted = ref(false)

const isEditing = computed(() => !!props.taskToEdit)

watch(
  () => props.show,
  (open) => {
    if (open) {
      if (props.taskToEdit) {
        formTitle.value = props.taskToEdit.title
        formSectionId.value = props.taskToEdit.section_id || ''
        formDifficulty.value = (props.taskToEdit.difficulty_points as 1 | 2 | 3 | 5) || 1
        formRepeat.value = props.taskToEdit.repeat || 'NONE'
        formNotes.value = props.taskToEdit.notes || ''
        formIsCompleted.value = props.taskToEdit.is_completed

        if (props.taskToEdit.due_date) {
          formDueDate.value = new Date(props.taskToEdit.due_date).toISOString().slice(0, 10)
        } else {
          formDueDate.value = ''
        }
      } else {
        formTitle.value = ''
        formSectionId.value = props.defaultSectionId || props.sections[0]?.id || ''
        formDifficulty.value = 1
        formRepeat.value = 'NONE'
        formDueDate.value = ''
        formNotes.value = ''
        formIsCompleted.value = false
      }
    }
  }
)

const onSubmit = () => {
  if (!formTitle.value.trim()) return
  emit('save', {
    id: props.taskToEdit?.id,
    title: formTitle.value.trim(),
    section_id: formSectionId.value || undefined,
    difficulty_points: formDifficulty.value,
    repeat: formRepeat.value,
    due_date: formDueDate.value ? new Date(formDueDate.value).toISOString() : undefined,
    notes: formNotes.value.trim() || undefined,
    is_completed: formIsCompleted.value
  })
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <div class="modal-header">
        <div class="modal-title-group">
          <h3 class="modal-title">{{ isEditing ? 'Editar Tarea' : 'Nueva Tarea' }}</h3>
          <span class="modal-subtitle">Añade dificultad, repetición y notas detalladas</span>
        </div>
        <button class="close-btn" @click="emit('close')">✕</button>
      </div>

      <form class="modal-form" @submit.prevent="onSubmit">
        <!-- Título -->
        <div class="form-group">
          <label class="form-label">Título de la Tarea *</label>
          <input
            v-model="formTitle"
            type="text"
            placeholder="ej. Pagar servicios de luz y agua"
            required
            maxlength="160"
            class="form-input"
          />
        </div>

        <!-- Sección y Dificultad -->
        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Lista / Sección</label>
            <select v-model="formSectionId" class="form-select">
              <option value="">Sin Sección</option>
              <option v-for="sec in sections" :key="sec.id" :value="sec.id">
                {{ sec.icon }} {{ sec.name }}
              </option>
            </select>
          </div>

          <div class="form-group flex-1">
            <label class="form-label">Dificultad / Esfuerzo</label>
            <select v-model="formDifficulty" class="form-select">
              <option :value="1">⚡ 1 pt (Rápida < 5 min)</option>
              <option :value="2">⚡ 2 pts (Fácil ~15 min)</option>
              <option :value="3">⚡ 3 pts (Media ~30 min)</option>
              <option :value="5">⚡ 5 pts (Exigente > 1 hr)</option>
            </select>
          </div>
        </div>

        <!-- Repetición y Fecha de Vencimiento -->
        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Frecuencia de Repetición</label>
            <select v-model="formRepeat" class="form-select">
              <option value="NONE">Sin Repetición</option>
              <option value="DAILY">Diaria</option>
              <option value="WEEKDAYS">Lunes a Viernes</option>
              <option value="WEEKLY">Semanal</option>
              <option value="MONTHLY">Mensual</option>
            </select>
          </div>

          <div class="form-group flex-1">
            <label class="form-label">Fecha de Vencimiento</label>
            <input
              v-model="formDueDate"
              type="date"
              class="form-input"
            />
          </div>
        </div>

        <!-- Notas / Pasos -->
        <div class="form-group">
          <label class="form-label">Notas o Sub-Pasos</label>
          <textarea
            v-model="formNotes"
            rows="3"
            placeholder="Añade instrucciones, enlaces o notas complementarias..."
            maxlength="1000"
            class="form-textarea"
          ></textarea>
        </div>

        <!-- Checkbox Completado (si edita) -->
        <div v-if="isEditing" class="completed-check-row">
          <label class="check-label">
            <input
              v-model="formIsCompleted"
              type="checkbox"
              class="form-checkbox"
            />
            <span>Marcar tarea como completada</span>
          </label>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button type="button" class="cancel-btn" @click="emit('close')">
            Cancelar
          </button>
          <button
            type="submit"
            class="submit-btn glow-teal"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ isEditing ? 'Guardar Cambios' : 'Crear Tarea' }}
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
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  animation: fadeIn 0.15s ease-out;
}

.modal-card {
  width: 100%;
  max-width: 500px;
  border-radius: 20px;
  padding: 24px;
  background: rgba(23, 23, 28, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-top: 3px solid var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
  animation: scaleUp 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0 0 4px 0;
}

.modal-subtitle {
  font-size: 0.8rem;
  color: var(--hermes-text-muted, #94949E);
}

.close-btn {
  background: rgba(255, 255, 255, 0.05);
  border: none;
  color: var(--hermes-text-muted, #94949E);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-group {
  margin-bottom: 14px;
}

.form-label {
  display: block;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--hermes-text-muted, #94949E);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 9px 12px;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.9rem;
  outline: none;
  transition: all 0.2s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  border-color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.03);
  box-shadow: 0 0 12px rgba(0, 255, 198, 0.15);
}

.form-select option {
  background: #17171c;
  color: #F4F4F5;
}

.form-row {
  display: flex;
  gap: 12px;
}

.flex-1 { flex: 1; }

.completed-check-row {
  margin-bottom: 14px;
}

.check-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--hermes-text-primary, #F4F4F5);
  cursor: pointer;
}

.form-checkbox {
  width: 18px;
  height: 18px;
  accent-color: var(--hermes-accent-teal, #00FFC6);
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.cancel-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted, #94949E);
  padding: 9px 16px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  padding: 9px 20px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 0.9rem;
  cursor: pointer;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
</style>

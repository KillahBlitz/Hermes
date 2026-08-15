<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { Epic, Task } from '~/composables/useBoards'

const props = defineProps<{
  show: boolean
  epics: Epic[]
  taskToEdit?: Task | null
  defaultStatus?: string
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: {
    id?: string
    title: string
    description?: string
    type: string
    complexity: string
    epic_id?: string
    status: string
    location: string
    due_date?: string
  }): void
}>()

const formTitle = ref('')
const formDesc = ref('')
const formType = ref<'IMPROVEMENT' | 'URGENT' | 'PENDING' | 'ANALYSIS'>('IMPROVEMENT')
const formComplexity = ref<'XS' | 'S' | 'M' | 'L' | 'XL'>('M')
const formEpicId = ref('')
const formStatus = ref('TODO')
const formLocation = ref('BOARD')
const formDueDate = ref('')

const isEditing = computed(() => !!props.taskToEdit)

watch(
  () => props.show,
  (open) => {
    if (open) {
      if (props.taskToEdit) {
        formTitle.value = props.taskToEdit.title
        formDesc.value = props.taskToEdit.description || ''
        formType.value = props.taskToEdit.type
        formComplexity.value = props.taskToEdit.complexity
        formEpicId.value = props.taskToEdit.epic_id || ''
        formStatus.value = props.taskToEdit.status
        formLocation.value = props.taskToEdit.location

        if (props.taskToEdit.due_date) {
          formDueDate.value = new Date(props.taskToEdit.due_date).toISOString().slice(0, 10)
        } else {
          formDueDate.value = ''
        }
      } else {
        formTitle.value = ''
        formDesc.value = ''
        formType.value = 'IMPROVEMENT'
        formComplexity.value = 'M'
        formEpicId.value = props.epics[0]?.id || ''
        formStatus.value = props.defaultStatus || 'TODO'
        formLocation.value = 'BOARD'
        formDueDate.value = ''
      }
    }
  }
)

const onSubmit = () => {
  if (!formTitle.value.trim()) return

  emit('save', {
    id: props.taskToEdit?.id,
    title: formTitle.value.trim(),
    description: formDesc.value.trim() || undefined,
    type: formType.value,
    complexity: formComplexity.value,
    epic_id: formEpicId.value || undefined,
    status: formStatus.value,
    location: formLocation.value,
    due_date: formDueDate.value ? new Date(formDueDate.value).toISOString() : undefined
  })
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel" :class="formType.toLowerCase()">
      <div class="modal-header">
        <div class="modal-title-group">
          <h3 class="modal-title">{{ isEditing ? 'Editar Tarea' : 'Nueva Tarea' }}</h3>
          <span class="modal-subtitle">Organiza y prioriza el trabajo en tu tablero</span>
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
            placeholder="ej. Diseñar arquitectura de base de datos"
            required
            maxlength="140"
            class="form-input"
          />
        </div>

        <!-- Descripción -->
        <div class="form-group">
          <label class="form-label">Descripción o Criterios de Aceptación</label>
          <textarea
            v-model="formDesc"
            rows="3"
            placeholder="Detalles, enlaces, requerimientos o notas técnicas..."
            maxlength="2000"
            class="form-textarea"
          ></textarea>
        </div>

        <!-- Tipo y Complejidad en 2 columnas -->
        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Tipo de Tarea *</label>
            <select v-model="formType" required class="form-select">
              <option value="IMPROVEMENT">🟢 Mejora</option>
              <option value="URGENT">🔴 Urgente</option>
              <option value="PENDING">🟡 Pendiente</option>
              <option value="ANALYSIS">🔵 Análisis</option>
            </select>
          </div>

          <div class="form-group flex-1">
            <label class="form-label">Nivel de Complejidad *</label>
            <select v-model="formComplexity" required class="form-select">
              <option value="XS">XS (Muy Baja / 1 pt)</option>
              <option value="S">S (Baja / 2 pts)</option>
              <option value="M">M (Media / 3 pts)</option>
              <option value="L">L (Alta / 5 pts)</option>
              <option value="XL">XL (Muy Alta / 8 pts)</option>
            </select>
          </div>
        </div>

        <!-- Épica y Fecha Límite -->
        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Épica Vinculada</label>
            <select v-model="formEpicId" class="form-select">
              <option value="">Sin Épica</option>
              <option v-for="ep in epics" :key="ep.id" :value="ep.id">
                {{ ep.icon }} {{ ep.name }}
              </option>
            </select>
          </div>

          <div class="form-group flex-1">
            <label class="form-label">Fecha Límite</label>
            <input
              v-model="formDueDate"
              type="date"
              class="form-input"
            />
          </div>
        </div>

        <!-- Ubicación y Estado -->
        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Ubicación</label>
            <select v-model="formLocation" class="form-select">
              <option value="BOARD">📌 Tablero Kanban</option>
              <option value="BACKLOG">📥 Cola de Backlog</option>
            </select>
          </div>

          <div v-if="formLocation === 'BOARD'" class="form-group flex-1">
            <label class="form-label">Columna Inicial</label>
            <select v-model="formStatus" class="form-select">
              <option value="TODO">📋 Por Hacer (ToDo)</option>
              <option value="IN_PROGRESS">⚡ En Progreso</option>
              <option value="TESTING">🧪 Por Probar (Testing)</option>
              <option value="DONE">✅ Finalizado (Done)</option>
            </select>
          </div>
        </div>

        <!-- Footer Acciones -->
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
  max-width: 540px;
  border-radius: 20px;
  padding: 24px;
  background: rgba(23, 23, 28, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
  animation: scaleUp 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.modal-card.improvement { border-top: 3px solid #00FFC6; }
.modal-card.urgent { border-top: 3px solid #FF007F; }
.modal-card.pending { border-top: 3px solid #FFD166; }
.modal-card.analysis { border-top: 3px solid #00E5FF; }

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

.close-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}

.form-group {
  margin-bottom: 16px;
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
  padding: 10px 14px;
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

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.cancel-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted, #94949E);
  padding: 10px 18px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  padding: 10px 22px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 0.92rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 0 16px rgba(0, 255, 198, 0.35);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
</style>

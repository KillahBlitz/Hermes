<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Milestone, MilestoneTopic } from '~/composables/useProgress'

const props = defineProps<{
  show: boolean
  milestoneToEdit?: Milestone | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', data: {
    title: string
    category: string
    icon: string
    color: string
    target_date: string
    description?: string
    topics: MilestoneTopic[]
  }): void
}>()

const title = ref('')
const category = ref('TITULACION')
const icon = ref('🎯')
const color = ref('#00FFC6')
const targetDate = ref('')
const description = ref('')
const topics = ref<MilestoneTopic[]>([])
const newTopicTitle = ref('')

const iconsList = ['🎓', '☁️', '📚', '🎯', '🚀', '⚡', '📊', '🛡️', '🏆', '🔥']

const colorOptions = [
  { value: '#00FFC6', label: 'Verde Neón' },
  { value: '#00E5FF', label: 'Azul Neón' },
  { value: '#FF007F', label: 'Rosa Neón' },
  { value: '#FFD166', label: 'Amarillo Neón' },
  { value: '#9D4EDD', label: 'Púrpura Neón' }
]

watch(() => props.milestoneToEdit, (item) => {
  if (item) {
    title.value = item.title
    category.value = item.category || 'TITULACION'
    icon.value = item.icon || '🎯'
    color.value = item.color || '#00FFC6'
    targetDate.value = item.target_date ? item.target_date.substring(0, 10) : ''
    description.value = item.description || ''
    topics.value = item.topics ? JSON.parse(JSON.stringify(item.topics)) : []
  } else {
    title.value = ''
    category.value = 'TITULACION'
    icon.value = '🎯'
    color.value = '#00FFC6'
    targetDate.value = ''
    description.value = ''
    topics.value = []
  }
  newTopicTitle.value = ''
}, { immediate: true })

const addTopic = () => {
  const t = newTopicTitle.value.trim()
  if (!t) return
  topics.value.push({
    id: `top_${Date.now()}_${Math.random().toString(36).substring(2, 5)}`,
    title: t,
    is_completed: false
  })
  newTopicTitle.value = ''
}

const removeTopic = (index: number) => {
  topics.value.splice(index, 1)
}

const handleSave = () => {
  if (!title.value.trim() || !targetDate.value) return
  emit('save', {
    title: title.value.trim(),
    category: category.value,
    icon: icon.value,
    color: color.value,
    target_date: new Date(targetDate.value).toISOString(),
    description: description.value.trim() || undefined,
    topics: topics.value
  })
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <div class="modal-header">
        <h3 class="modal-title">
          {{ milestoneToEdit ? 'Editar Hito Estratégico' : 'Nuevo Hito de Gran Escala' }}
        </h3>
        <button type="button" class="close-btn" @click="emit('close')">✕</button>
      </div>

      <form class="modal-form" @submit.prevent="handleSave">
        <div class="form-group">
          <label class="form-label">Título del Proyecto / Hito *</label>
          <input
            v-model="title"
            type="text"
            class="form-input"
            placeholder="ej. Proyecto de Titulación de Ingeniería en Computación"
            required
          >
        </div>

        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Categoría *</label>
            <select v-model="category" class="form-select">
              <option value="TITULACION">🎓 Titulación</option>
              <option value="CERTIFICACION">☁️ Certificación</option>
              <option value="EXAMEN">📚 Examen Crítico</option>
              <option value="PROYECTO">🎯 Proyecto Macro</option>
              <option value="CARRERA">🚀 Carrera Backend</option>
            </select>
          </div>

          <div class="form-group flex-1">
            <label class="form-label">Fecha Meta (Deadline) *</label>
            <input
              v-model="targetDate"
              type="date"
              class="form-input"
              required
            >
          </div>
        </div>

        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Icono</label>
            <div class="icon-picker">
              <button
                v-for="ic in iconsList"
                :key="ic"
                type="button"
                class="icon-btn"
                :class="{ 'is-selected': icon === ic }"
                @click="icon = ic"
              >
                {{ ic }}
              </button>
            </div>
          </div>

          <div class="form-group flex-1">
            <label class="form-label">Color de Acento</label>
            <div class="color-picker-row">
              <button
                v-for="c in colorOptions"
                :key="c.value"
                type="button"
                class="color-btn"
                :class="{ 'is-selected': color === c.value }"
                :style="{ backgroundColor: c.value }"
                :title="c.label"
                @click="color = c.value"
              />
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Descripción</label>
          <textarea
            v-model="description"
            class="form-textarea"
            placeholder="Detalles, enlaces de estudio o contexto de este objetivo..."
            rows="2"
          />
        </div>

        <!-- Topics & Deliverables Builder -->
        <div class="form-group">
          <label class="form-label">Temario y Entregables ({{ topics.length }})</label>
          <div class="add-topic-row">
            <input
              v-model="newTopicTitle"
              type="text"
              class="form-input flex-1"
              placeholder="ej. Capítulo 2: Marco Teórico y Arquitectura"
              @keydown.enter.prevent="addTopic"
            >
            <button
              type="button"
              class="add-topic-btn btn-neon-blue"
              @click="addTopic"
            >
              ＋ Agregar
            </button>
          </div>

          <!-- Topics List -->
          <div v-if="topics.length > 0" class="modal-topics-list">
            <div
              v-for="(t, idx) in topics"
              :key="t.id"
              class="modal-topic-item"
            >
              <span class="topic-index">{{ idx + 1 }}.</span>
              <span class="topic-text">{{ t.title }}</span>
              <button
                type="button"
                class="remove-topic-btn"
                @click="removeTopic(idx)"
              >
                ✕
              </button>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="emit('close')">Cancelar</button>
          <button type="submit" class="btn-neon-teal">
            {{ milestoneToEdit ? 'Actualizar Hito' : 'Crear Hito' }}
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
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.modal-card {
  width: 100%;
  max-width: 540px;
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
  margin-bottom: 20px;
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

.form-row {
  display: flex;
  gap: 12px;
}

.flex-1 {
  flex: 1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--hermes-text-muted);
}

.form-input,
.form-select,
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

.icon-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.icon-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 4px 6px;
  font-size: 0.95rem;
  cursor: pointer;
}

.icon-btn.is-selected {
  background: rgba(0, 255, 198, 0.2);
  border-color: var(--hermes-accent-teal, #00FFC6);
}

.color-picker-row {
  display: flex;
  gap: 8px;
  align-items: center;
  height: 38px;
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
}

.add-topic-row {
  display: flex;
  gap: 8px;
}

.add-topic-btn {
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}

.modal-topics-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 160px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.2);
  padding: 8px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.modal-topic-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 8px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.03);
  font-size: 0.8rem;
}

.topic-index {
  color: var(--hermes-text-muted);
  font-weight: 700;
}

.topic-text {
  flex: 1;
  color: var(--hermes-text-primary);
}

.remove-topic-btn {
  background: rgba(255, 77, 77, 0.12);
  border: 1px solid rgba(255, 77, 77, 0.25);
  color: #ff4d4d;
  font-size: 0.75rem;
  font-weight: 700;
  width: 22px;
  height: 22px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-topic-btn:hover {
  background: rgba(255, 77, 77, 0.28);
  border-color: #ff4d4d;
  transform: scale(1.05);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 14px;
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

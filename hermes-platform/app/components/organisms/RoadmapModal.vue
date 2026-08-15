<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Roadmap } from '~/composables/useProgress'

const props = defineProps<{
  show: boolean
  roadmapToEdit?: Roadmap | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', data: {
    title: string
    description?: string
    category: string
    color: string
  }): void
}>()

const title = ref('')
const description = ref('')
const category = ref('Backend')
const color = ref('#00FFC6')

const colorOptions = [
  { value: '#00FFC6', label: 'Teal Neón' },
  { value: '#00E5FF', label: 'Azul Neón' },
  { value: '#FF007F', label: 'Rosa Neón' },
  { value: '#FFD166', label: 'Amarillo Neón' },
  { value: '#9D4EDD', label: 'Púrpura Neón' }
]

watch(() => props.roadmapToEdit, (item) => {
  if (item) {
    title.value = item.title
    description.value = item.description || ''
    category.value = item.category || 'Backend'
    color.value = item.color || '#00FFC6'
  } else {
    title.value = ''
    description.value = ''
    category.value = 'Backend'
    color.value = '#00FFC6'
  }
}, { immediate: true })

const handleSave = () => {
  if (!title.value.trim()) return
  emit('save', {
    title: title.value.trim(),
    description: description.value.trim() || undefined,
    category: category.value.trim() || 'General',
    color: color.value
  })
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <div class="modal-header">
        <h3 class="modal-title">
          {{ roadmapToEdit ? 'Editar Árbol de Mapas' : 'Nueva Ruta de Aprendizaje' }}
        </h3>
        <button type="button" class="close-btn" @click="emit('close')">✕</button>
      </div>

      <form class="modal-form" @submit.prevent="handleSave">
        <div class="form-group">
          <label class="form-label">Título de la Ruta *</label>
          <input
            v-model="title"
            type="text"
            class="form-input"
            placeholder="ej. Especialización en Arquitectura Backend y Microservicios"
            required
          >
        </div>

        <div class="form-group">
          <label class="form-label">Categoría</label>
          <input
            v-model="category"
            type="text"
            class="form-input"
            placeholder="ej. Backend, Cloud AWS, Machine Learning"
          >
        </div>

        <div class="form-group">
          <label class="form-label">Descripción o Metas</label>
          <textarea
            v-model="description"
            class="form-textarea"
            placeholder="Alcance, objetivos y tecnologías a dominar en esta ruta..."
            rows="3"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Color Representativo</label>
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

        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="emit('close')">Cancelar</button>
          <button type="submit" class="btn-neon-blue">
            {{ roadmapToEdit ? 'Actualizar Ruta' : 'Crear Ruta' }}
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
  max-width: 500px;
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
  gap: 16px;
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
.form-textarea {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 10px 12px;
  color: var(--hermes-text-primary);
  font-size: 0.88rem;
  outline: none;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  border-color: rgba(0, 229, 255, 0.4);
}

.color-picker-row {
  display: flex;
  gap: 10px;
}

.color-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.color-btn.is-selected {
  transform: scale(1.2);
  border-color: #fff;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.modal-actions {
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
</style>

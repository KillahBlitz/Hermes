<script setup lang="ts">
import { ref, watch } from 'vue'
import type { RoadmapNode } from '~/composables/useProgress'

const props = defineProps<{
  show: boolean
  nodeToEdit?: RoadmapNode | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', nodeData: {
    id?: string
    title: string
    icon: string
    color: string
    status: 'PENDIENTE' | 'EN_CURSO' | 'DOMINADO'
    description?: string
  }): void
}>()

const title = ref('')
const icon = ref('⚡')
const color = ref('#00E5FF')
const status = ref<'PENDIENTE' | 'EN_CURSO' | 'DOMINADO'>('PENDIENTE')
const description = ref('')

const iconsList = ['⚡', '🛡️', '⚙️', '☁️', '🚀', '🧠', '📦', '🎯', '🔥', '📊']

const colorOptions = [
  { value: '#00E5FF', label: 'Azul Neón' },
  { value: '#00FFC6', label: 'Verde Neón' },
  { value: '#FF007F', label: 'Rosa Neón' },
  { value: '#FFD166', label: 'Amarillo Neón' },
  { value: '#9D4EDD', label: 'Púrpura Neón' }
]

watch(() => props.nodeToEdit, (item) => {
  if (item) {
    title.value = item.title
    icon.value = item.icon || '⚡'
    color.value = item.color || '#00E5FF'
    status.value = item.status || 'PENDIENTE'
    description.value = item.description || ''
  } else {
    title.value = ''
    icon.value = '⚡'
    color.value = '#00E5FF'
    status.value = 'PENDIENTE'
    description.value = ''
  }
}, { immediate: true })

const handleSave = () => {
  if (!title.value.trim()) return
  emit('save', {
    id: props.nodeToEdit?.id,
    title: title.value.trim(),
    icon: icon.value,
    color: color.value,
    status: status.value,
    description: description.value.trim() || undefined
  })
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <div class="modal-header">
        <h3 class="modal-title">
          {{ nodeToEdit ? 'Editar Módulo del Roadmap' : 'Nuevo Módulo / Tema' }}
        </h3>
        <button type="button" class="close-btn" @click="emit('close')">✕</button>
      </div>

      <form class="modal-form" @submit.prevent="handleSave">
        <div class="form-group">
          <label class="form-label">Título del Módulo *</label>
          <input
            v-model="title"
            type="text"
            class="form-input"
            placeholder="ej. Patrones de Concurrencia y Canales"
            required
          >
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
            <label class="form-label">Estado</label>
            <select v-model="status" class="form-select">
              <option value="PENDIENTE">Pendiente</option>
              <option value="EN_CURSO">En curso</option>
              <option value="DOMINADO">Dominado</option>
            </select>
          </div>
        </div>

        <div class="form-group">
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

        <div class="form-group">
          <label class="form-label">Descripción Corta</label>
          <textarea
            v-model="description"
            class="form-textarea"
            placeholder="Resumen o conceptos clave que cubre este módulo..."
            rows="2"
          />
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="emit('close')">Cancelar</button>
          <button type="submit" class="btn-neon-blue">
            {{ nodeToEdit ? 'Guardar Cambios' : 'Agregar Módulo' }}
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
  max-width: 480px;
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
  font-size: 0.88rem;
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
  font-size: 1rem;
  cursor: pointer;
}

.icon-btn.is-selected {
  background: rgba(0, 229, 255, 0.2);
  border-color: var(--hermes-accent-blue, #00E5FF);
}

.color-picker-row {
  display: flex;
  gap: 10px;
}

.color-btn {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.color-btn.is-selected {
  transform: scale(1.2);
  border-color: #fff;
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

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { TodoSection } from '~/composables/useLists'

const props = defineProps<{
  show: boolean
  sectionToEdit?: TodoSection | null
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: { id?: string; name: string; icon: string; color: string }): void
}>()

const formName = ref('')
const formIcon = ref('📋')
const formColor = ref('#00E5FF')

const EMOJI_PALETTE = ['☀️', '🔁', '🏠', '💼', '🛒', '🎓', '🎯', '✨', '⚡', '🏋️', '📚', '💰']
const COLOR_PALETTE = ['#00E5FF', '#00FFC6', '#FF007F', '#FFD166', '#7209B7', '#118AB2', '#F72585', '#06D6A0']

const isEditing = computed(() => !!props.sectionToEdit)

watch(
  () => props.show,
  (open) => {
    if (open) {
      if (props.sectionToEdit) {
        formName.value = props.sectionToEdit.name
        formIcon.value = props.sectionToEdit.icon || '📋'
        formColor.value = props.sectionToEdit.color || '#00E5FF'
      } else {
        formName.value = ''
        formIcon.value = '📋'
        formColor.value = '#00E5FF'
      }
    }
  }
)

const onSubmit = () => {
  if (!formName.value.trim()) return
  emit('save', {
    id: props.sectionToEdit?.id,
    name: formName.value.trim(),
    icon: formIcon.value,
    color: formColor.value
  })
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <div class="modal-header">
        <div class="modal-title-group">
          <h3 class="modal-title">{{ isEditing ? 'Editar Sección' : 'Nueva Sección / Lista' }}</h3>
          <span class="modal-subtitle">Organiza tus tareas y rutinas por categorías temáticas</span>
        </div>
        <button class="close-btn" @click="emit('close')">✕</button>
      </div>

      <form class="modal-form" @submit.prevent="onSubmit">
        <!-- Nombre -->
        <div class="form-group">
          <label class="form-label">Nombre de la Lista / Sección *</label>
          <input
            v-model="formName"
            type="text"
            placeholder="ej. Finanzas del Hogar, Compras Semanales..."
            required
            maxlength="60"
            class="form-input"
          />
        </div>

        <!-- Selector Icono -->
        <div class="palette-row">
          <span class="palette-label">Icono:</span>
          <div class="emojis-picker">
            <button
              v-for="em in EMOJI_PALETTE"
              :key="em"
              type="button"
              class="emoji-btn"
              :class="{ active: formIcon === em }"
              @click="formIcon = em"
            >
              {{ em }}
            </button>
          </div>
        </div>

        <!-- Selector Color -->
        <div class="palette-row">
          <span class="palette-label">Color Neón:</span>
          <div class="colors-picker">
            <button
              v-for="c in COLOR_PALETTE"
              :key="c"
              type="button"
              class="color-btn"
              :class="{ active: formColor === c }"
              :style="{ backgroundColor: c }"
              @click="formColor = c"
            ></button>
          </div>
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
            {{ isEditing ? 'Guardar Cambios' : 'Crear Sección' }}
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
  max-width: 480px;
  border-radius: 20px;
  padding: 24px;
  background: rgba(23, 23, 28, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-top: 3px solid var(--hermes-accent-blue, #00E5FF);
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

.form-input {
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

.form-input:focus {
  border-color: var(--hermes-accent-blue, #00E5FF);
  background: rgba(0, 229, 255, 0.03);
  box-shadow: 0 0 12px rgba(0, 229, 255, 0.15);
}

.palette-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.palette-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--hermes-text-muted, #94949E);
  min-width: 65px;
}

.emojis-picker {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.emoji-btn {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid transparent;
  border-radius: 6px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  cursor: pointer;
}

.emoji-btn.active {
  border-color: var(--hermes-accent-blue, #00E5FF);
  background: rgba(0, 229, 255, 0.15);
}

.colors-picker {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.color-btn {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
}

.color-btn.active {
  border-color: #fff;
  transform: scale(1.2);
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
  padding: 10px 18px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn {
  background: var(--hermes-accent-blue, #00E5FF);
  color: #0c0c0e;
  border: none;
  padding: 10px 22px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 0.92rem;
  cursor: pointer;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
</style>

<script setup lang="ts">
import { ref } from 'vue'
import type { Epic } from '~/composables/useBoards'
import EpicBadge from '~/components/atoms/EpicBadge.vue'

const props = defineProps<{
  show: boolean
  epics: Epic[]
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'create', payload: { name: string; description?: string; color: string; icon: string }): void
  (e: 'delete', epicId: string): void
}>()

const newName = ref('')
const newDesc = ref('')
const newIcon = ref('💼')
const newColor = ref('#00E5FF')

const EMOJI_PALETTE = ['🎓', '💼', '📚', '🚀', '💻', '🧪', '📱', '⚙️', '🎨', '🔥', '💡', '🏆']
const COLOR_PALETTE = ['#00E5FF', '#00FFC6', '#FF007F', '#FFD166', '#7209B7', '#118AB2', '#F72585', '#06D6A0']

const onCreateEpic = () => {
  if (!newName.value.trim()) return
  emit('create', {
    name: newName.value.trim(),
    description: newDesc.value.trim() || undefined,
    icon: newIcon.value,
    color: newColor.value
  })
  newName.value = ''
  newDesc.value = ''
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <div class="modal-header">
        <div class="modal-title-group">
          <h3 class="modal-title">Gestor de Épicas</h3>
          <span class="modal-subtitle">Organiza tus proyectos escolares, laborales y personales</span>
        </div>
        <button class="close-btn" @click="emit('close')">✕</button>
      </div>

      <!-- Formulario Nueva Épica -->
      <div class="new-epic-box">
        <h4 class="box-title">Crear Nueva Épica</h4>
        <div class="new-epic-form">
          <div class="input-row">
            <div class="selected-icon-preview">
              <span class="icon-char">{{ newIcon }}</span>
            </div>

            <input
              v-model="newName"
              type="text"
              placeholder="Nombre de la épica..."
              maxlength="60"
              class="form-input flex-1"
              @keydown.enter.prevent="onCreateEpic"
            />

            <button
              class="add-btn glow-teal"
              :disabled="!newName.trim() || loading"
              @click="onCreateEpic"
            >
              + Agregar
            </button>
          </div>

          <input
            v-model="newDesc"
            type="text"
            placeholder="Descripción corta de la iniciativa (opcional)..."
            maxlength="200"
            class="form-input desc-input"
          />

          <!-- Selector Icono -->
          <div class="palette-row">
            <span class="palette-label">Icono:</span>
            <div class="emojis-picker">
              <button
                v-for="em in EMOJI_PALETTE"
                :key="em"
                type="button"
                class="emoji-btn"
                :class="{ active: newIcon === em }"
                @click="newIcon = em"
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
                :class="{ active: newColor === c }"
                :style="{ backgroundColor: c }"
                @click="newColor = c"
              ></button>
            </div>
          </div>
        </div>
      </div>

      <!-- Lista de Épicas Existentes -->
      <div class="epics-list-box">
        <h4 class="box-title">Épicas Registradas ({{ epics.length }})</h4>
        <div class="epics-grid">
          <div
            v-for="ep in epics"
            :key="ep.id"
            class="epic-item-row"
          >
            <div class="epic-info">
              <EpicBadge :name="ep.name" :icon="ep.icon" :color="ep.color" size="md" />
              <span v-if="ep.description" class="epic-desc-text">{{ ep.description }}</span>
            </div>

            <div class="epic-actions">
              <span class="tasks-counter-badge">{{ ep.task_count || 0 }} tareas</span>
              <span v-if="ep.is_default" class="default-pill" title="Épica base">Base</span>
              <button
                v-else
                class="delete-epic-btn"
                title="Eliminar épica personalizada"
                @click="emit('delete', ep.id)"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      </div>
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
  max-width: 580px;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 20px;
  padding: 24px;
  background: rgba(23, 23, 28, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.12);
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

.close-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}

.box-title {
  font-size: 0.82rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--hermes-text-muted, #94949E);
  margin-bottom: 12px;
}

.new-epic-box {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 20px;
}

.new-epic-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.input-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.selected-icon-preview {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.form-input {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 9px 14px;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.88rem;
  outline: none;
}

.form-input:focus {
  border-color: var(--hermes-accent-teal, #00FFC6);
}

.desc-input {
  font-size: 0.82rem;
}

.flex-1 { flex: 1; }

.add-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  font-weight: 800;
  font-size: 0.82rem;
  padding: 9px 14px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.palette-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.palette-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--hermes-text-muted, #94949E);
  min-width: 65px;
}

.emojis-picker {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.emoji-btn {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid transparent;
  border-radius: 6px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
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
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
}

.color-btn.active {
  border-color: #fff;
  transform: scale(1.2);
}

.epics-list-box {
  display: flex;
  flex-direction: column;
}

.epics-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 220px;
  overflow-y: auto;
}

.epic-item-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.epic-info {
  display: flex;
  align-items: center;
  gap: 10px;
  overflow: hidden;
}

.epic-desc-text {
  font-size: 0.75rem;
  color: var(--hermes-text-muted, #94949E);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 240px;
}

.epic-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tasks-counter-badge {
  font-size: 0.72rem;
  font-family: 'JetBrains Mono', monospace;
  color: var(--hermes-text-muted, #94949E);
}

.default-pill {
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--hermes-text-muted, #94949E);
  background: rgba(255, 255, 255, 0.06);
  padding: 2px 6px;
  border-radius: 4px;
}

.delete-epic-btn {
  background: rgba(255, 0, 127, 0.1);
  border: 1px solid rgba(255, 0, 127, 0.2);
  color: var(--hermes-accent-pink, #FF007F);
  width: 22px;
  height: 22px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
}

.delete-epic-btn:hover {
  background: var(--hermes-accent-pink, #FF007F);
  color: #fff;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
</style>

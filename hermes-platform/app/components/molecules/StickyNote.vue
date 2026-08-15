<script setup lang="ts">
import { ref, watch } from 'vue'
import type { StickyNote } from '~/composables/useBoards'

const props = defineProps<{
  note: StickyNote
}>()

const emit = defineEmits<{
  (e: 'update', id: string, payload: Partial<StickyNote>): void
  (e: 'updatePosition', id: string, x: number, y: number, zIndex?: number): void
  (e: 'delete', id: string): void
}>()

const localTitle = ref(props.note.title || '')
const localContent = ref(props.note.content)
const showColorPicker = ref(false)
const isDragging = ref(false)

const COLOR_PALETTE = [
  '#FFD166', // Amarillo Cyber
  '#00FFC6', // Verde Teal
  '#FF007F', // Rosa Neón
  '#00E5FF', // Azul Neón
  '#B5179E', // Morado
  '#06D6A0', // Verde Esmeralda
  '#F72585'  // Magenta
]

watch(() => props.note.title, (val) => { localTitle.value = val || '' })
watch(() => props.note.content, (val) => { localContent.value = val })

const onSaveContent = () => {
  if (localContent.value !== props.note.content || localTitle.value !== props.note.title) {
    emit('update', props.note.id, {
      title: localTitle.value.trim(),
      content: localContent.value.trim()
    })
  }
}

const onSelectColor = (c: string) => {
  emit('update', props.note.id, { color: c })
  showColorPicker.value = false
}

// Drag & Drop Handling
const startDrag = (event: MouseEvent | TouchEvent) => {
  isDragging.value = true
  const clientX = 'touches' in event && event.touches[0] ? event.touches[0].clientX : (event as MouseEvent).clientX
  const clientY = 'touches' in event && event.touches[0] ? event.touches[0].clientY : (event as MouseEvent).clientY

  const startX = clientX
  const startY = clientY
  const initX = props.note.x
  const initY = props.note.y

  const onMove = (e: MouseEvent | TouchEvent) => {
    if (!isDragging.value) return
    const curX = 'touches' in e && e.touches[0] ? e.touches[0].clientX : (e as MouseEvent).clientX
    const curY = 'touches' in e && e.touches[0] ? e.touches[0].clientY : (e as MouseEvent).clientY

    const dx = curX - startX
    const dy = curY - startY

    const newX = Math.max(0, initX + dx)
    const newY = Math.max(0, initY + dy)

    emit('updatePosition', props.note.id, newX, newY, 50)
  }

  const onEnd = () => {
    isDragging.value = false
    window.removeEventListener('mousemove', onMove)
    window.removeEventListener('mouseup', onEnd)
    window.removeEventListener('touchmove', onMove)
    window.removeEventListener('touchend', onEnd)
  }

  window.addEventListener('mousemove', onMove)
  window.addEventListener('mouseup', onEnd)
  window.addEventListener('touchmove', onMove)
  window.addEventListener('touchend', onEnd)
}
</script>

<template>
  <div
    class="sticky-note-card"
    :style="{
      left: `${note.x}px`,
      top: `${note.y}px`,
      zIndex: note.z_index,
      transform: `rotate(${note.rotation}deg)`,
      backgroundColor: `${note.color}15`,
      borderColor: `${note.color}50`,
      boxShadow: `0 8px 24px rgba(0, 0, 0, 0.6), 0 0 16px ${note.color}20`
    }"
  >
    <!-- Tape / Header de Arrastre -->
    <div
      class="sticky-header-tape"
      :style="{ backgroundColor: `${note.color}35`, borderColor: `${note.color}60` }"
      @mousedown="startDrag"
      @touchstart="startDrag"
    >
      <div class="tape-dots">
        <span></span><span></span><span></span>
      </div>

      <div class="note-actions" @mousedown.stop @touchstart.stop>
        <!-- Selector de Color -->
        <div class="color-picker-wrapper">
          <button
            type="button"
            class="color-btn"
            :style="{ backgroundColor: note.color }"
            title="Cambiar color"
            @click="showColorPicker = !showColorPicker"
          ></button>

          <div v-if="showColorPicker" class="color-popover glass-panel">
            <button
              v-for="c in COLOR_PALETTE"
              :key="c"
              type="button"
              class="palette-dot"
              :style="{ backgroundColor: c }"
              @click="onSelectColor(c)"
            ></button>
          </div>
        </div>

        <!-- Botón Eliminar -->
        <button
          type="button"
          class="delete-note-btn"
          title="Eliminar post-it"
          @click="emit('delete', note.id)"
        >
          ✕
        </button>
      </div>
    </div>

    <!-- Título de la Nota -->
    <input
      v-model="localTitle"
      type="text"
      placeholder="Título de la idea..."
      maxlength="60"
      class="note-title-input"
      :style="{ color: note.color }"
      @blur="onSaveContent"
    />

    <!-- Contenido Textarea -->
    <textarea
      v-model="localContent"
      placeholder="Escribe tu idea aquí..."
      rows="4"
      class="note-body-textarea"
      @blur="onSaveContent"
    ></textarea>
  </div>
</template>

<style scoped>
.sticky-note-card {
  position: absolute;
  width: 220px;
  min-height: 180px;
  border-radius: 12px;
  border: 1px solid;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  flex-direction: column;
  padding: 10px 12px 14px;
  gap: 8px;
  transition: box-shadow 0.2s ease;
  user-select: none;
}

.sticky-note-card:hover {
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.8), 0 0 24px rgba(255, 255, 255, 0.15) !important;
}

.sticky-header-tape {
  height: 22px;
  border-radius: 6px;
  border: 1px solid;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 8px;
  cursor: grab;
}

.sticky-header-tape:active {
  cursor: grabbing;
}

.tape-dots {
  display: flex;
  align-items: center;
  gap: 3px;
}

.tape-dots span {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
}

.note-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.color-picker-wrapper {
  position: relative;
}

.color-btn {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 0;
}

.color-popover {
  position: absolute;
  top: calc(100% + 6px);
  right: -20px;
  z-index: 50;
  display: flex;
  gap: 6px;
  padding: 6px;
  border-radius: 8px;
  background: rgba(23, 23, 28, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
}

.palette-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 1px solid transparent;
  cursor: pointer;
  transition: transform 0.1s ease;
}

.palette-dot:hover {
  transform: scale(1.2);
  border-color: #fff;
}

.delete-note-btn {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.7rem;
  font-weight: 800;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 2px;
  transition: color 0.15s ease;
}

.delete-note-btn:hover {
  color: var(--hermes-accent-pink, #FF007F);
}

.note-title-input {
  background: transparent;
  border: none;
  outline: none;
  font-weight: 800;
  font-size: 0.88rem;
  padding: 2px 0;
  letter-spacing: -0.01em;
}

.note-title-input::placeholder {
  color: var(--hermes-text-muted, #94949E);
  opacity: 0.5;
}

.note-body-textarea {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.82rem;
  line-height: 1.4;
  resize: none;
  font-family: inherit;
}

.note-body-textarea::placeholder {
  color: var(--hermes-text-muted, #94949E);
  opacity: 0.5;
}
</style>

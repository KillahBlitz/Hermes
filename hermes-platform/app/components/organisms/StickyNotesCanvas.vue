<script setup lang="ts">
import { ref } from 'vue'
import type { StickyNote } from '~/composables/useBoards'
import StickyNoteComp from '~/components/molecules/StickyNote.vue'

const props = defineProps<{
  notes: StickyNote[]
  loading?: boolean
}>()

const emit = defineEmits<{
  createNote: [payload: { title?: string; content: string; color: string; x: number; y: number }]
  updateNote: [id: string, payload: Partial<StickyNote>]
  updatePosition: [id: string, x: number, y: number, zIndex?: number]
  deleteNote: [id: string]
}>()

const canvasRef = ref<HTMLElement | null>(null)

const handleCanvasDoubleClick = (e: MouseEvent) => {
  if (!canvasRef.value) return
  const rect = canvasRef.value.getBoundingClientRect()
  const x = Math.max(20, e.clientX - rect.left - 100)
  const y = Math.max(20, e.clientY - rect.top - 40)

  emit('createNote', {
    title: 'Nueva Idea',
    content: '',
    color: '#FFD166',
    x,
    y
  })
}

const handleQuickAdd = () => {
  // Posición aleatoria cerca del centro
  const randomX = 120 + Math.floor(Math.random() * 200)
  const randomY = 100 + Math.floor(Math.random() * 150)
  const colors = ['#FFD166', '#00FFC6', '#FF007F', '#00E5FF', '#B5179E']
  const randomColor: string = colors[Math.floor(Math.random() * colors.length)] ?? '#FFD166'

  emit('createNote', {
    title: '',
    content: 'Escribe tu nueva idea aquí...',
    color: randomColor,
    x: randomX,
    y: randomY
  })
}
</script>

<template>
  <div class="sticky-canvas-wrapper">
    <!-- Top Floating Toolbar -->
    <div class="canvas-floating-toolbar glass-panel">
      <div class="toolbar-info">
        <span class="toolbar-icon">💡</span>
        <span class="toolbar-text">Pizarrón de Ideas Libres (Arrastra en cualquier área o haz doble clic para fijar)</span>
      </div>

      <button class="primary-btn glow-teal" @click="handleQuickAdd">
        <span>+</span> Nuevo Post-it
      </button>
    </div>

    <!-- Canvas Area -->
    <div
      ref="canvasRef"
      class="canvas-work-area"
      @dblclick="handleCanvasDoubleClick"
    >
      <div v-if="notes.length === 0" class="canvas-empty-hint">
        <span>📌</span>
        <p>Haz doble clic en cualquier punto del pizarrón o pulsa "+ Nuevo Post-it" para fijar tus ideas.</p>
      </div>

      <StickyNoteComp
        v-for="note in notes"
        :key="note.id"
        :note="note"
        @update="(id, payload) => emit('updateNote', id, payload)"
        @update-position="(id, x, y, zIndex) => emit('updatePosition', id, x, y, zIndex)"
        @delete="(id) => emit('deleteNote', id)"
      />
    </div>
  </div>
</template>

<style scoped>
.sticky-canvas-wrapper {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.canvas-floating-toolbar {
  padding: 12px 20px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.toolbar-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.toolbar-icon { font-size: 1.2rem; }

.toolbar-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--hermes-text-primary, #F4F4F5);
}

.primary-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  font-weight: 800;
  font-size: 0.85rem;
  padding: 8px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 16px rgba(0, 255, 198, 0.4);
}

/* Área de Canvas */
.canvas-work-area {
  position: relative;
  width: 100%;
  min-height: 650px;
  border-radius: 16px;
  background: radial-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px), #111115;
  background-size: 24px 24px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
  box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.8);
}

.canvas-empty-hint {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: var(--hermes-text-muted, #94949E);
  pointer-events: none;
  opacity: 0.5;
  max-width: 320px;
}

.canvas-empty-hint span {
  font-size: 2.2rem;
  margin-bottom: 8px;
}

.canvas-empty-hint p {
  font-size: 0.88rem;
  margin: 0;
}
</style>

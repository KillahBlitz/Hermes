<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import type { Roadmap, RoadmapNode, RoadmapEdge } from '~/composables/useProgress'
import RoadmapNodeCard from '~/components/molecules/RoadmapNodeCard.vue'

const props = defineProps<{
  roadmaps: Roadmap[]
  activeRoadmap: Roadmap | null
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'selectRoadmap', id: string): void
  (e: 'createRoadmap'): void
  (e: 'editRoadmap', roadmap: Roadmap): void
  (e: 'deleteRoadmap', roadmap: Roadmap): void
  (e: 'createNode', roadmap: Roadmap): void
  (e: 'editNode', roadmap: Roadmap, node: RoadmapNode): void
  (e: 'deleteNode', roadmap: Roadmap, node: RoadmapNode): void
  (e: 'openNote', node: RoadmapNode): void
  (e: 'updateRoadmapData', roadmap: Roadmap): void
}>()

// Canvas Zoom & Pan
const zoom = ref(1.0)
const panX = ref(0)
const panY = ref(0)
const isPanning = ref(false)
const startPanX = ref(0)
const startPanY = ref(0)

// Dragging Node
const draggingNodeId = ref<string | null>(null)
const dragStartX = ref(0)
const dragStartY = ref(0)
const nodeInitialX = ref(0)
const nodeInitialY = ref(0)

// Connecting Mode
const connectSourceNode = ref<RoadmapNode | null>(null)

// Selected Node
const selectedNodeId = ref<string | null>(null)

const canvasContainer = ref<HTMLElement | null>(null)

// Nodes & Edges from active roadmap
const currentNodes = computed(() => props.activeRoadmap?.nodes || [])
const currentEdges = computed(() => props.activeRoadmap?.edges || [])

// ─────────────────────────────────────────────────────────────
// PAN & ZOOM HANDLING
// ─────────────────────────────────────────────────────────────

const handleWheel = (e: WheelEvent) => {
  if (e.ctrlKey || e.metaKey || true) {
    e.preventDefault()
    const zoomDelta = e.deltaY > 0 ? -0.08 : 0.08
    const newZoom = Math.min(Math.max(zoom.value + zoomDelta, 0.4), 2.0)
    zoom.value = Math.round(newZoom * 100) / 100
  }
}

const startPan = (e: MouseEvent) => {
  // Only pan if clicking canvas background
  if ((e.target as HTMLElement).closest('.roadmap-node-card')) return
  isPanning.value = true
  startPanX.value = e.clientX - panX.value
  startPanY.value = e.clientY - panY.value
}

const handleMouseMove = (e: MouseEvent) => {
  if (isPanning.value) {
    panX.value = e.clientX - startPanX.value
    panY.value = e.clientY - startPanY.value
  } else if (draggingNodeId.value && props.activeRoadmap) {
    const dx = (e.clientX - dragStartX.value) / zoom.value
    const dy = (e.clientY - dragStartY.value) / zoom.value
    const node = props.activeRoadmap.nodes.find(n => n.id === draggingNodeId.value)
    if (node) {
      node.x = Math.round(nodeInitialX.value + dx)
      node.y = Math.round(nodeInitialY.value + dy)
    }
  }
}

const handleMouseUp = () => {
  if (isPanning.value) {
    isPanning.value = false
  }
  if (draggingNodeId.value && props.activeRoadmap) {
    draggingNodeId.value = null
    emit('updateRoadmapData', props.activeRoadmap)
  }
}

const handleMouseDownNode = (e: MouseEvent, node: RoadmapNode) => {
  e.stopPropagation()
  if (connectSourceNode.value) {
    // Si estamos en modo conexión, conectar con este nodo objetivo
    if (connectSourceNode.value.id !== node.id && props.activeRoadmap) {
      const exists = props.activeRoadmap.edges.some(
        edge => edge.source_node_id === connectSourceNode.value!.id && edge.target_node_id === node.id
      )
      if (!exists) {
        props.activeRoadmap.edges.push({
          id: `edge_${Date.now()}`,
          source_node_id: connectSourceNode.value.id,
          target_node_id: node.id
        })
        emit('updateRoadmapData', props.activeRoadmap)
      }
    }
    connectSourceNode.value = null
    return
  }

  selectedNodeId.value = node.id
  draggingNodeId.value = node.id
  dragStartX.value = e.clientX
  dragStartY.value = e.clientY
  nodeInitialX.value = node.x
  nodeInitialY.value = node.y
}

const resetView = () => {
  zoom.value = 1.0
  panX.value = 0
  panY.value = 0
}

const handleStartConnect = (node: RoadmapNode) => {
  connectSourceNode.value = node
}

const removeEdge = (edgeId: string) => {
  if (!props.activeRoadmap) return
  props.activeRoadmap.edges = props.activeRoadmap.edges.filter(e => e.id !== edgeId)
  emit('updateRoadmapData', props.activeRoadmap)
}

// Helper to compute SVG Path between two nodes
const computeEdgePath = (edge: RoadmapEdge) => {
  const src = currentNodes.value.find(n => n.id === edge.source_node_id)
  const tgt = currentNodes.value.find(n => n.id === edge.target_node_id)
  if (!src || !tgt) return ''

  const nodeWidth = 260
  const nodeHeight = 110

  const x1 = src.x + nodeWidth
  const y1 = src.y + nodeHeight / 2
  const x2 = tgt.x
  const y2 = tgt.y + nodeHeight / 2

  const dx = Math.abs(x2 - x1) * 0.5
  return `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('mouseup', handleMouseUp)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseup', handleMouseUp)
})
</script>

<template>
  <div class="roadmap-canvas-view">
    <!-- Top Canvas Toolbar -->
    <div class="canvas-toolbar glass-panel">
      <!-- Roadmap Selector & Metadata -->
      <div class="toolbar-left">
        <div class="roadmap-select-wrapper">
          <label class="select-label">Ruta:</label>
          <select
            v-if="roadmaps.length > 0"
            class="roadmap-select"
            :value="activeRoadmap?.id"
            @change="emit('selectRoadmap', ($event.target as HTMLSelectElement).value)"
          >
            <option v-for="r in roadmaps" :key="r.id" :value="r.id">
              {{ r.title }} ({{ r.nodes?.length || 0 }} módulos)
            </option>
          </select>
        </div>

        <button
          type="button"
          class="toolbar-btn secondary-btn"
          title="Crear nuevo árbol de mapas"
          @click="emit('createRoadmap')"
        >
          <span>＋ Nueva Ruta</span>
        </button>

        <button
          v-if="activeRoadmap"
          type="button"
          class="toolbar-btn icon-btn"
          title="Editar información de la ruta"
          @click="emit('editRoadmap', activeRoadmap)"
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
        </button>
      </div>

      <!-- Action Buttons & Zoom Controls -->
      <div class="toolbar-right">
        <button
          v-if="activeRoadmap"
          type="button"
          class="toolbar-btn primary-neon-btn"
          @click="emit('createNode', activeRoadmap)"
        >
          <span class="btn-icon">⚡</span>
          <span>Agregar Módulo</span>
        </button>

        <div class="zoom-controls">
          <button type="button" class="zoom-btn" title="Alejar" @click="zoom = Math.max(zoom - 0.15, 0.4)">−</button>
          <span class="zoom-level" @click="resetView">{{ Math.round(zoom * 100) }}%</span>
          <button type="button" class="zoom-btn" title="Acercar" @click="zoom = Math.min(zoom + 0.15, 2.0)">＋</button>
          <button type="button" class="zoom-btn reset-btn" title="Restablecer vista" @click="resetView">⟲</button>
        </div>
      </div>
    </div>

    <!-- Connection Banner in connect mode -->
    <div v-if="connectSourceNode" class="connect-banner glass-panel">
      <span>🔗 Haz clic en el módulo destino para conectar desde <strong>"{{ connectSourceNode.title }}"</strong></span>
      <button type="button" class="cancel-connect-btn" @click="connectSourceNode = null">Cancelar</button>
    </div>

    <!-- Main Canvas Viewport -->
    <div
      ref="canvasContainer"
      class="canvas-viewport"
      :class="{ 'is-panning': isPanning, 'is-connecting': !!connectSourceNode }"
      @wheel="handleWheel"
      @mousedown="startPan"
    >
      <!-- Infinite Grid Plane with Transforms -->
      <div
        class="canvas-plane"
        :style="{
          transform: `translate(${panX}px, ${panY}px) scale(${zoom})`,
          transformOrigin: '0 0'
        }"
      >
        <!-- SVG Connections Layer -->
        <svg class="canvas-svg-layer">
          <defs>
            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="7"
              refX="9"
              refY="3.5"
              orient="auto"
            >
              <polygon points="0 0, 10 3.5, 0 7" fill="#00E5FF" />
            </marker>
          </defs>

          <!-- Render Edges -->
          <g v-for="edge in currentEdges" :key="edge.id" class="edge-group">
            <path
              :d="computeEdgePath(edge)"
              class="edge-path"
              marker-end="url(#arrowhead)"
            />
            <!-- Delete edge hover zone -->
            <path
              :d="computeEdgePath(edge)"
              class="edge-hover-zone"
              @click.stop="removeEdge(edge.id)"
            />
          </g>
        </svg>

        <!-- Render Roadmap Nodes -->
        <RoadmapNodeCard
          v-for="node in currentNodes"
          :key="node.id"
          :node="node"
          :is-selected="selectedNodeId === node.id"
          @mousedown="handleMouseDownNode($event, node)"
          @select="selectedNodeId = node.id"
          @open-note="emit('openNote', node)"
          @edit="emit('editNode', activeRoadmap!, node)"
          @delete="emit('deleteNode', activeRoadmap!, node)"
          @start-connect="handleStartConnect"
        />

        <!-- Empty Canvas Hint -->
        <div v-if="currentNodes.length === 0" class="canvas-empty-hint">
          <span class="hint-icon">🗺️</span>
          <p class="hint-title">Pizarrón de Ruta Vacío</p>
          <p class="hint-desc">Presiona "+ Agregar Módulo" para comenzar a trazar tu árbol de conocimientos.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.roadmap-canvas-view {
  position: relative;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 210px);
  min-height: 550px;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: #08080a;
}

.canvas-toolbar {
  position: absolute;
  top: 14px;
  left: 14px;
  right: 14px;
  z-index: 30;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  border-radius: 12px;
  background: rgba(23, 23, 28, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  flex-wrap: wrap;
  gap: 10px;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.roadmap-select-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
}

.select-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--hermes-text-muted);
}

.roadmap-select {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: var(--hermes-text-primary);
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  outline: none;
}

.toolbar-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-primary);
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.12);
}

.primary-neon-btn {
  background: rgba(0, 229, 255, 0.15);
  border: 1px solid var(--hermes-accent-blue, #00E5FF);
  color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 12px rgba(0, 229, 255, 0.25);
}

.primary-neon-btn:hover {
  background: rgba(0, 229, 255, 0.25);
  box-shadow: 0 0 16px rgba(0, 229, 255, 0.4);
}

.icon-btn {
  padding: 6px 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted);
}

.icon-btn:hover {
  color: var(--hermes-text-primary);
  background: rgba(255, 255, 255, 0.1);
}

.zoom-controls {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  overflow: hidden;
}

.zoom-btn {
  background: none;
  border: none;
  color: var(--hermes-text-muted);
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 700;
}

.zoom-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-primary);
}

.zoom-level {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
  padding: 0 6px;
  cursor: pointer;
  user-select: none;
  font-feature-settings: 'tnum';
}

.connect-banner {
  position: absolute;
  top: 70px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 35;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 8px 18px;
  border-radius: 999px;
  background: rgba(0, 255, 198, 0.15);
  border: 1px solid var(--hermes-accent-teal, #00FFC6);
  color: var(--hermes-text-primary);
  font-size: 0.82rem;
  box-shadow: 0 0 20px rgba(0, 255, 198, 0.3);
}

.cancel-connect-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: var(--hermes-text-primary);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  cursor: pointer;
}

.canvas-viewport {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  cursor: default;
  background-image: 
    radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
  background-size: 28px 28px;
}

.canvas-viewport.is-panning {
  cursor: grab;
}

.canvas-viewport.is-connecting {
  cursor: crosshair;
}

.canvas-plane {
  position: absolute;
  top: 0;
  left: 0;
  width: 4000px;
  height: 4000px;
}

.canvas-svg-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 5;
}

.edge-group {
  pointer-events: auto;
}

.edge-path {
  fill: none;
  stroke: var(--hermes-accent-blue, #00E5FF);
  stroke-width: 2.5;
  stroke-linecap: round;
  filter: drop-shadow(0 0 6px rgba(0, 229, 255, 0.6));
  transition: stroke 0.2s ease;
}

.edge-hover-zone {
  fill: none;
  stroke: transparent;
  stroke-width: 18;
  cursor: pointer;
}

.edge-hover-zone:hover + .edge-path,
.edge-group:hover .edge-path {
  stroke: var(--hermes-accent-pink, #FF007F);
  stroke-dasharray: 4 4;
}

.canvas-empty-hint {
  position: absolute;
  top: 240px;
  left: 360px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--hermes-text-muted);
  user-select: none;
}

.hint-icon {
  font-size: 3rem;
  opacity: 0.6;
}

.hint-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
}

.hint-desc {
  margin: 0;
  font-size: 0.85rem;
}
</style>

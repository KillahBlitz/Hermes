<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import type { KnowledgeGraphData, GraphNode, GraphEdge } from '~/composables/useProgress'

const props = defineProps<{
  graphData: KnowledgeGraphData
}>()

const emit = defineEmits<{
  (e: 'selectNode', nodeTitle: string): void
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
const selectedTag = ref<string>('')
const hoveredNode = ref<any | null>(null)

// Simulation nodes with physics coordinates
interface SimNode {
  id: string
  title: string
  tags: string[]
  connections_count: number
  x: number
  y: number
  vx: number
  vy: number
  radius: number
  color: string
}

interface SimEdge {
  source: SimNode
  target: SimNode
}

let animationFrameId: number | null = null
let nodes: SimNode[] = []
let edges: SimEdge[] = []

// Canvas Pan & Zoom
const scale = ref(1.0)
const panX = ref(0)
const panY = ref(0)
let isDraggingCanvas = false
let dragStartX = 0
let dragStartY = 0
let draggedNode: SimNode | null = null

const initSimulation = () => {
  const canvas = canvasRef.value
  if (!canvas) return

  const width = canvas.clientWidth || 800
  const height = canvas.clientHeight || 500
  canvas.width = width * window.devicePixelRatio
  canvas.height = height * window.devicePixelRatio

  const rawNodes = props.graphData.nodes || []
  const rawEdges = props.graphData.edges || []

  // Filter by tag if selected
  const filteredRawNodes = selectedTag.value
    ? rawNodes.filter(n => n.tags.includes(selectedTag.value))
    : rawNodes

  const nodeMap = new Map<string, SimNode>()

  nodes = filteredRawNodes.map((n, i) => {
    const angle = (i / Math.max(filteredRawNodes.length, 1)) * 2 * Math.PI
    const dist = 120 + Math.random() * 150
    const nodeObj: SimNode = {
      id: n.id,
      title: n.title,
      tags: n.tags,
      connections_count: n.connections_count,
      x: width / 2 + Math.cos(angle) * dist,
      y: height / 2 + Math.sin(angle) * dist,
      vx: 0,
      vy: 0,
      radius: Math.min(Math.max(14 + n.connections_count * 4, 14), 28),
      color: n.connections_count > 2 ? '#00FFC6' : '#00E5FF'
    }
    nodeMap.set(n.id, nodeObj)
    return nodeObj
  })

  edges = []
  for (const e of rawEdges) {
    const src = nodeMap.get(e.source)
    const tgt = nodeMap.get(e.target)
    if (src && tgt) {
      edges.push({ source: src, target: tgt })
    }
  }
}

const updatePhysics = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  const width = canvas.clientWidth
  const height = canvas.clientHeight

  // Repulsion between nodes
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i]
      const b = nodes[j]
      if (!a || !b) continue
      const dx = b.x - a.x
      const dy = b.y - a.y
      const dist = Math.sqrt(dx * dx + dy * dy) || 1
      if (dist < 300) {
        const force = 120 / (dist * dist)
        const fx = (dx / dist) * force
        const fy = (dy / dist) * force
        a.vx -= fx
        a.vy -= fy
        b.vx += fx
        b.vy += fy
      }
    }
  }

  // Edge springs
  for (const e of edges) {
    const dx = e.target.x - e.source.x
    const dy = e.target.y - e.source.y
    const dist = Math.sqrt(dx * dx + dy * dy) || 1
    const targetDist = 90
    const force = (dist - targetDist) * 0.04
    const fx = (dx / dist) * force
    const fy = (dy / dist) * force
    e.source.vx += fx
    e.source.vy += fy
    e.target.vx -= fx
    e.target.vy -= fy
  }

  // Center gravity & damping
  for (const n of nodes) {
    if (n === draggedNode) continue
    const dx = width / 2 - n.x
    const dy = height / 2 - n.y
    n.vx += dx * 0.002
    n.vy += dy * 0.002
    n.vx *= 0.88
    n.vy *= 0.88
    n.x += n.vx
    n.y += n.vy
  }
}

const renderCanvas = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const dpr = window.devicePixelRatio || 1
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  ctx.save()
  ctx.scale(dpr * scale.value, dpr * scale.value)
  ctx.translate(panX.value, panY.value)

  // Draw Edges
  for (const e of edges) {
    ctx.beginPath()
    ctx.moveTo(e.source.x, e.source.y)
    ctx.lineTo(e.target.x, e.target.y)
    ctx.strokeStyle = 'rgba(0, 229, 255, 0.25)'
    ctx.lineWidth = 1.5
    ctx.stroke()
  }

  // Draw Nodes
  for (const n of nodes) {
    const isHovered = hoveredNode.value?.id === n.id

    // Glow circle
    ctx.beginPath()
    ctx.arc(n.x, n.y, n.radius + (isHovered ? 4 : 0), 0, 2 * Math.PI)
    ctx.fillStyle = isHovered ? '#FF007F' : n.color
    ctx.shadowColor = isHovered ? '#FF007F' : n.color
    ctx.shadowBlur = isHovered ? 18 : 8
    ctx.fill()
    ctx.shadowBlur = 0

    // Inner dark center
    ctx.beginPath()
    ctx.arc(n.x, n.y, n.radius * 0.7, 0, 2 * Math.PI)
    ctx.fillStyle = '#0c0c0e'
    ctx.fill()

    // Title label
    ctx.font = isHovered ? 'bold 12px Inter, sans-serif' : '600 11px Inter, sans-serif'
    ctx.fillStyle = isHovered ? '#00FFC6' : '#F4F4F5'
    ctx.textAlign = 'center'
    ctx.fillText(n.title, n.x, n.y + n.radius + 14)
  }

  ctx.restore()
}

const loop = () => {
  updatePhysics()
  renderCanvas()
  animationFrameId = requestAnimationFrame(loop)
}

// Mouse events
const handleMouseDown = (e: MouseEvent) => {
  const canvas = canvasRef.value
  if (!canvas) return
  const rect = canvas.getBoundingClientRect()
  const mouseX = (e.clientX - rect.left - panX.value * scale.value) / scale.value
  const mouseY = (e.clientY - rect.top - panY.value * scale.value) / scale.value

  // Check if clicking a node
  for (const n of nodes) {
    const dx = mouseX - n.x
    const dy = mouseY - n.y
    if (Math.sqrt(dx * dx + dy * dy) <= n.radius) {
      draggedNode = n
      return
    }
  }

  isDraggingCanvas = true
  dragStartX = e.clientX - panX.value
  dragStartY = e.clientY - panY.value
}

const handleMouseMove = (e: MouseEvent) => {
  const canvas = canvasRef.value
  if (!canvas) return
  const rect = canvas.getBoundingClientRect()
  const mouseX = (e.clientX - rect.left - panX.value * scale.value) / scale.value
  const mouseY = (e.clientY - rect.top - panY.value * scale.value) / scale.value

  if (draggedNode) {
    draggedNode.x = mouseX
    draggedNode.y = mouseY
    draggedNode.vx = 0
    draggedNode.vy = 0
    return
  }

  if (isDraggingCanvas) {
    panX.value = (e.clientX - dragStartX)
    panY.value = (e.clientY - dragStartY)
    return
  }

  // Hover detection
  let found = null
  for (const n of nodes) {
    const dx = mouseX - n.x
    const dy = mouseY - n.y
    if (Math.sqrt(dx * dx + dy * dy) <= n.radius + 4) {
      found = n
      break
    }
  }
  hoveredNode.value = found
  canvas.style.cursor = found ? 'pointer' : isDraggingCanvas ? 'grabbing' : 'default'
}

const handleMouseUp = (e: MouseEvent) => {
  if (draggedNode) {
    // If clicked without large drag, open note!
    emit('selectNode', draggedNode.title)
    draggedNode = null
  }
  isDraggingCanvas = false
}

const handleWheel = (e: WheelEvent) => {
  e.preventDefault()
  const zoomDelta = e.deltaY > 0 ? -0.1 : 0.1
  scale.value = Math.min(Math.max(scale.value + zoomDelta, 0.4), 2.5)
}

watch(() => props.graphData, () => {
  initSimulation()
}, { deep: true })

watch(selectedTag, () => {
  initSimulation()
})

onMounted(() => {
  initSimulation()
  loop()
})

onUnmounted(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }
})
</script>

<template>
  <div class="knowledge-graph-view glass-panel">
    <!-- Top Graph Controls -->
    <div class="graph-header">
      <div class="header-left">
        <h4 class="graph-title">🌐 Grafo de Conocimiento Interactivo (2D)</h4>
        <span class="graph-kpi">{{ graphData.total_notes }} notas · {{ graphData.total_connections }} conexiones</span>
      </div>

      <div class="tags-filter">
        <button
          type="button"
          class="tag-filter-btn"
          :class="{ 'is-active': selectedTag === '' }"
          @click="selectedTag = ''"
        >
          #todas
        </button>
        <button
          v-for="tag in graphData.all_tags"
          :key="tag"
          type="button"
          class="tag-filter-btn"
          :class="{ 'is-active': selectedTag === tag }"
          @click="selectedTag = tag"
        >
          #{{ tag }}
        </button>
      </div>
    </div>

    <!-- Canvas Simulation Area -->
    <div class="graph-canvas-container">
      <canvas
        ref="canvasRef"
        class="graph-canvas"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @wheel="handleWheel"
      />

      <div class="canvas-help-hint">
        <span>💡 Arrastra nodos para explorar · Haz clic en un nodo para abrir su nota Markdown</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.knowledge-graph-view {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 220px);
  min-height: 520px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  overflow: hidden;
  position: relative;
}

.graph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  flex-wrap: wrap;
  gap: 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.graph-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
}

.graph-kpi {
  font-size: 0.78rem;
  color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.1);
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid rgba(0, 255, 198, 0.25);
  font-weight: 600;
}

.tags-filter {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.tag-filter-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted);
  font-size: 0.75rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.tag-filter-btn:hover {
  color: var(--hermes-accent-blue, #00E5FF);
  border-color: rgba(0, 229, 255, 0.3);
}

.tag-filter-btn.is-active {
  background: rgba(0, 229, 255, 0.18);
  border-color: var(--hermes-accent-blue, #00E5FF);
  color: var(--hermes-accent-blue, #00E5FF);
}

.graph-canvas-container {
  position: relative;
  flex: 1;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #08080a;
}

.graph-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

.canvas-help-hint {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(12, 12, 14, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 0.75rem;
  color: var(--hermes-text-muted);
  pointer-events: none;
  backdrop-filter: blur(8px);
}
</style>

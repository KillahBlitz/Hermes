<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const props = withDefaults(
  defineProps<{
    particleCount?: number
    maxDistance?: number
    interactive?: boolean
  }>(),
  {
    particleCount: 45,
    maxDistance: 120,
    interactive: true
  }
)

const canvasRef = ref<HTMLCanvasElement | null>(null)
let animationFrameId: number | null = null

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  radius: number
  color: string
  alpha: number
  alphaSpeed: number
}

const colors: string[] = [
  'rgba(0, 229, 255, ',   // Blue neon
  'rgba(255, 0, 127, ',   // Pink neon
  'rgba(0, 255, 198, ',   // Teal neon
  'rgba(255, 255, 255, '  // White subtle
]

let particles: Particle[] = []
const mouse = { x: -1000, y: -1000, radius: 140 }

const initParticles = (width: number, height: number) => {
  particles = []
  const count = props.particleCount
  for (let i = 0; i < count; i++) {
    const baseColor = colors[Math.floor(Math.random() * colors.length)] || 'rgba(0, 229, 255, '
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.45,
      vy: (Math.random() - 0.5) * 0.45,
      radius: Math.random() * 2 + 1,
      color: baseColor,
      alpha: Math.random() * 0.5 + 0.2,
      alphaSpeed: (Math.random() * 0.008 + 0.003) * (Math.random() > 0.5 ? 1 : -1)
    })
  }
}

const handleResize = () => {
  if (!canvasRef.value) return
  const canvas = canvasRef.value
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight
  initParticles(canvas.width, canvas.height)
}

const handleMouseMove = (e: MouseEvent) => {
  mouse.x = e.clientX
  mouse.y = e.clientY
}

const handleMouseLeave = () => {
  mouse.x = -1000
  mouse.y = -1000
}

const render = () => {
  if (!canvasRef.value) return
  const canvas = canvasRef.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  const width = canvas.width
  const height = canvas.height
  const maxDist = props.maxDistance

  // Update and draw particles
  for (let i = 0; i < particles.length; i++) {
    const p = particles[i]
    if (!p) continue

    // Movement
    p.x += p.vx
    p.y += p.vy

    // Wrap around boundaries
    if (p.x < 0) p.x = width
    else if (p.x > width) p.x = 0
    if (p.y < 0) p.y = height
    else if (p.y > height) p.y = 0

    // Alpha pulsing
    p.alpha += p.alphaSpeed
    if (p.alpha > 0.7 || p.alpha < 0.15) {
      p.alphaSpeed = -p.alphaSpeed
    }

    // Mouse gentle repulsion
    if (props.interactive) {
      const dx = mouse.x - p.x
      const dy = mouse.y - p.y
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist < mouse.radius && dist > 0) {
        const force = (mouse.radius - dist) / mouse.radius
        p.x -= (dx / dist) * force * 1.5
        p.y -= (dy / dist) * force * 1.5
      }
    }

    // Draw particle circle with glow
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2)
    ctx.fillStyle = `${p.color}${p.alpha})`
    ctx.shadowBlur = 8
    ctx.shadowColor = `${p.color}0.8)`
    ctx.fill()
    ctx.shadowBlur = 0

    // Connect with nearby particles
    for (let j = i + 1; j < particles.length; j++) {
      const p2 = particles[j]
      if (!p2) continue
      const dx = p.x - p2.x
      const dy = p.y - p2.y
      const dist = Math.sqrt(dx * dx + dy * dy)

      if (dist < maxDist) {
        const lineAlpha = (1 - dist / maxDist) * 0.18
        ctx.beginPath()
        ctx.moveTo(p.x, p.y)
        ctx.lineTo(p2.x, p2.y)
        ctx.strokeStyle = `rgba(0, 229, 255, ${lineAlpha})`
        ctx.lineWidth = 0.8
        ctx.stroke()
      }
    }

    // Connect with mouse cursor
    if (props.interactive) {
      const dxMouse = p.x - mouse.x
      const dyMouse = p.y - mouse.y
      const distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse)
      if (distMouse < mouse.radius) {
        const mouseLineAlpha = (1 - distMouse / mouse.radius) * 0.25
        ctx.beginPath()
        ctx.moveTo(p.x, p.y)
        ctx.lineTo(mouse.x, mouse.y)
        ctx.strokeStyle = `rgba(255, 0, 127, ${mouseLineAlpha})`
        ctx.lineWidth = 1
        ctx.stroke()
      }
    }
  }

  animationFrameId = requestAnimationFrame(render)
}

onMounted(() => {
  if (typeof window !== 'undefined' && canvasRef.value) {
    handleResize()
    window.addEventListener('resize', handleResize)
    if (props.interactive) {
      window.addEventListener('mousemove', handleMouseMove, { passive: true })
      window.addEventListener('mouseleave', handleMouseLeave)
    }
    animationFrameId = requestAnimationFrame(render)
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', handleResize)
    if (props.interactive) {
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('mouseleave', handleMouseLeave)
    }
    if (animationFrameId !== null) {
      cancelAnimationFrame(animationFrameId)
    }
  }
})
</script>

<template>
  <canvas ref="canvasRef" class="hermes-particles-canvas" />
</template>

<style scoped>
.hermes-particles-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}
</style>

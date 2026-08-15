<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    points: 1 | 2 | 3 | 5 | number
    size?: 'sm' | 'md'
  }>(),
  {
    size: 'md'
  }
)

const config = computed(() => {
  switch (props.points) {
    case 1:
      return { label: '1 pt (Rápida)', color: '#00FFC6', bg: 'rgba(0, 255, 198, 0.1)' }
    case 2:
      return { label: '2 pts (Fácil)', color: '#00E5FF', bg: 'rgba(0, 229, 255, 0.1)' }
    case 3:
      return { label: '3 pts (Media)', color: '#FFD166', bg: 'rgba(255, 209, 102, 0.1)' }
    case 5:
      return { label: '5 pts (Exigente)', color: '#FF007F', bg: 'rgba(255, 0, 127, 0.1)' }
    default:
      return { label: `${props.points} pts`, color: '#94949E', bg: 'rgba(255, 255, 255, 0.05)' }
  }
})
</script>

<template>
  <span
    class="difficulty-pill"
    :class="size"
    :style="{
      color: config.color,
      backgroundColor: config.bg,
      borderColor: `${config.color}35`
    }"
    :title="`Esfuerzo estimado: ${config.label}`"
  >
    <span class="pts-icon">⚡</span>
    <span class="pts-text">{{ points }} {{ points === 1 ? 'pt' : 'pts' }}</span>
  </span>
</template>

<style scoped>
.difficulty-pill {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  border-radius: 6px;
  border: 1px solid;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  white-space: nowrap;
}

.difficulty-pill.sm {
  padding: 1px 6px;
  font-size: 0.7rem;
}

.difficulty-pill.md {
  padding: 2px 8px;
  font-size: 0.75rem;
}

.pts-icon {
  font-size: 0.75em;
}

.pts-text {
  line-height: 1;
}
</style>

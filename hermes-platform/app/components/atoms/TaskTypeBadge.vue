<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    type: 'IMPROVEMENT' | 'URGENT' | 'PENDING' | 'ANALYSIS' | string
    size?: 'sm' | 'md'
  }>(),
  {
    size: 'md'
  }
)

const config = computed(() => {
  switch (props.type) {
    case 'IMPROVEMENT':
      return { label: 'Mejora', icon: '🟢', color: '#00FFC6', bg: 'rgba(0, 255, 198, 0.12)', border: 'rgba(0, 255, 198, 0.3)' }
    case 'URGENT':
      return { label: 'Urgente', icon: '🔴', color: '#FF007F', bg: 'rgba(255, 0, 127, 0.12)', border: 'rgba(255, 0, 127, 0.3)' }
    case 'PENDING':
      return { label: 'Pendiente', icon: '🟡', color: '#FFD166', bg: 'rgba(255, 209, 102, 0.12)', border: 'rgba(255, 209, 102, 0.3)' }
    case 'ANALYSIS':
      return { label: 'Análisis', icon: '🔵', color: '#00E5FF', bg: 'rgba(0, 229, 255, 0.12)', border: 'rgba(0, 229, 255, 0.3)' }
    default:
      return { label: props.type, icon: '🏷️', color: '#94949E', bg: 'rgba(255, 255, 255, 0.05)', border: 'rgba(255, 255, 255, 0.1)' }
  }
})
</script>

<template>
  <span
    class="task-type-badge"
    :class="size"
    :style="{
      color: config.color,
      backgroundColor: config.bg,
      borderColor: config.border,
      boxShadow: `0 0 10px ${config.color}15`
    }"
  >
    <span class="type-icon">{{ config.icon }}</span>
    <span class="type-label">{{ config.label }}</span>
  </span>
</template>

<style scoped>
.task-type-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  border-radius: 8px;
  border: 1px solid;
  font-weight: 700;
  white-space: nowrap;
  letter-spacing: 0.02em;
}

.task-type-badge.sm {
  padding: 2px 7px;
  font-size: 0.72rem;
}

.task-type-badge.md {
  padding: 3px 9px;
  font-size: 0.78rem;
}

.type-icon {
  font-size: 0.75em;
}

.type-label {
  line-height: 1;
}
</style>

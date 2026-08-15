<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    priority: 'ALTA' | 'MEDIA' | 'BAJA' | string
    size?: 'sm' | 'md'
  }>(),
  {
    size: 'md'
  }
)

const config = computed(() => {
  switch (props.priority) {
    case 'ALTA':
      return { label: 'Alta', icon: '🔥', color: '#FF007F', bg: 'rgba(255, 0, 127, 0.12)', border: 'rgba(255, 0, 127, 0.3)' }
    case 'MEDIA':
      return { label: 'Media', icon: '⚡', color: '#FFD166', bg: 'rgba(255, 209, 102, 0.12)', border: 'rgba(255, 209, 102, 0.3)' }
    case 'BAJA':
      return { label: 'Baja', icon: '💤', color: '#00E5FF', bg: 'rgba(0, 229, 255, 0.12)', border: 'rgba(0, 229, 255, 0.3)' }
    default:
      return { label: props.priority, icon: '🏷️', color: '#94949E', bg: 'rgba(255, 255, 255, 0.05)', border: 'rgba(255, 255, 255, 0.1)' }
  }
})
</script>

<template>
  <span
    class="priority-badge"
    :class="size"
    :style="{
      color: config.color,
      backgroundColor: config.bg,
      borderColor: config.border
    }"
  >
    <span class="icon">{{ config.icon }}</span>
    <span class="label">{{ config.label }}</span>
  </span>
</template>

<style scoped>
.priority-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border-radius: 6px;
  border: 1px solid;
  font-weight: 700;
  white-space: nowrap;
}

.priority-badge.sm {
  padding: 2px 6px;
  font-size: 0.72rem;
}

.priority-badge.md {
  padding: 3px 8px;
  font-size: 0.78rem;
}

.icon { font-size: 0.8em; }
.label { line-height: 1; }
</style>

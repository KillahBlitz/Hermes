<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: 'PENDIENTE' | 'EN_CURSO' | 'DOMINADO' | string
}>()

const statusConfig = computed(() => {
  switch (props.status) {
    case 'DOMINADO':
      return {
        label: 'Dominado',
        color: '#00FFC6',
        bg: 'rgba(0, 255, 198, 0.12)',
        border: 'rgba(0, 255, 198, 0.35)',
        icon: '✓'
      }
    case 'EN_CURSO':
      return {
        label: 'En curso',
        color: '#00E5FF',
        bg: 'rgba(0, 229, 255, 0.12)',
        border: 'rgba(0, 229, 255, 0.35)',
        icon: '⚡'
      }
    default:
      return {
        label: 'Pendiente',
        color: '#94949E',
        bg: 'rgba(148, 148, 158, 0.12)',
        border: 'rgba(148, 148, 158, 0.25)',
        icon: '○'
      }
  }
})
</script>

<template>
  <span
    class="roadmap-status-badge"
    :style="{
      color: statusConfig.color,
      backgroundColor: statusConfig.bg,
      borderColor: statusConfig.border
    }"
  >
    <span class="status-icon">{{ statusConfig.icon }}</span>
    <span class="status-label">{{ statusConfig.label }}</span>
  </span>
</template>

<style scoped>
.roadmap-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  border-width: 1px;
  border-style: solid;
  letter-spacing: 0.02em;
  white-space: nowrap;
}

.status-icon {
  font-size: 0.7rem;
}
</style>

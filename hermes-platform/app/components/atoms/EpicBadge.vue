<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    name: string
    icon?: string
    color?: string
    size?: 'sm' | 'md'
  }>(),
  {
    icon: '💼',
    color: '#00E5FF',
    size: 'md'
  }
)

const tagStyles = computed(() => {
  const c = props.color || '#00E5FF'
  return {
    color: c,
    backgroundColor: `${c}15`,
    borderColor: `${c}35`,
    boxShadow: `0 0 10px ${c}12`
  }
})
</script>

<template>
  <span class="epic-badge" :class="size" :style="tagStyles" :title="`Épica: ${name}`">
    <span class="epic-icon">{{ icon }}</span>
    <span class="epic-name">{{ name }}</span>
  </span>
</template>

<style scoped>
.epic-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  border-radius: 8px;
  border: 1px solid transparent;
  font-weight: 700;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.epic-badge.sm {
  padding: 2px 7px;
  font-size: 0.72rem;
}

.epic-badge.md {
  padding: 3px 9px;
  font-size: 0.78rem;
}

.epic-icon {
  font-size: 0.85em;
}

.epic-name {
  line-height: 1;
}
</style>

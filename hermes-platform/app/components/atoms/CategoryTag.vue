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
    icon: '🏷️',
    color: '#00FFC6',
    size: 'md'
  }
)

const tagStyles = computed(() => {
  const c = props.color || '#00FFC6'
  return {
    color: c,
    backgroundColor: `${c}18`, // 10% opacity
    borderColor: `${c}40`, // 25% opacity
    boxShadow: `0 0 10px ${c}15`
  }
})
</script>

<template>
  <span class="category-tag" :class="size" :style="tagStyles">
    <span class="category-icon">{{ icon }}</span>
    <span class="category-name">{{ name }}</span>
  </span>
</template>

<style scoped>
.category-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 8px;
  border: 1px solid transparent;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.category-tag.sm {
  padding: 2px 8px;
  font-size: 0.75rem;
}

.category-tag.md {
  padding: 4px 10px;
  font-size: 0.82rem;
}

.category-icon {
  font-size: 0.9em;
}

.category-name {
  line-height: 1;
}
</style>

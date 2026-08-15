<script setup lang="ts">
import type { BreadcrumbItem } from '~/composables/useDriveBucket'

defineProps<{
  breadcrumbs: BreadcrumbItem[]
}>()

const emit = defineEmits<{
  (e: 'navigate', index: number): void
}>()
</script>

<template>
  <nav class="drive-breadcrumbs">
    <div class="breadcrumb-root-icon">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
      </svg>
    </div>

    <template v-for="(item, index) in breadcrumbs" :key="item.id">
      <span v-if="index > 0" class="breadcrumb-separator">/</span>
      <button
        class="breadcrumb-item-btn"
        :class="{ active: index === breadcrumbs.length - 1 }"
        type="button"
        @click="emit('navigate', index)"
      >
        {{ item.name }}
      </button>
    </template>
  </nav>
</template>

<style scoped>
.drive-breadcrumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  font-size: 0.88rem;
  overflow-x: auto;
  white-space: nowrap;
}

.breadcrumb-root-icon {
  color: var(--hermes-accent-teal);
  display: flex;
  align-items: center;
}

.breadcrumb-separator {
  color: rgba(255, 255, 255, 0.2);
  font-size: 0.8rem;
}

.breadcrumb-item-btn {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted);
  font-family: inherit;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.breadcrumb-item-btn:hover {
  color: var(--hermes-text-primary);
  background: rgba(255, 255, 255, 0.06);
}

.breadcrumb-item-btn.active {
  color: var(--hermes-accent-blue);
  font-weight: 700;
  pointer-events: none;
}
</style>

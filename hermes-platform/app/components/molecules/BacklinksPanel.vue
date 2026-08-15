<script setup lang="ts">
import type { BacklinkItem } from '~/composables/useProgress'

const props = defineProps<{
  backlinks: BacklinkItem[]
}>()

const emit = defineEmits<{
  (e: 'navigate', backlink: BacklinkItem): void
}>()
</script>

<template>
  <div class="backlinks-panel">
    <div class="backlinks-header">
      <div class="header-title-row">
        <span class="header-icon">🔗</span>
        <h4 class="header-title">Menciones y Backlinks</h4>
      </div>
      <span class="backlinks-count">{{ backlinks.length }}</span>
    </div>

    <div v-if="backlinks.length === 0" class="backlinks-empty">
      <p>Ninguna otra nota de la bóveda enlaza a esta nota aún.</p>
      <span class="hint">Usa <code>[[{{ 'Título de esta nota' }}]]</code> en otros apuntes para vincularlas.</span>
    </div>

    <div v-else class="backlinks-list">
      <button
        v-for="item in backlinks"
        :key="item.id"
        type="button"
        class="backlink-item"
        @click="emit('navigate', item)"
      >
        <span class="item-arrow">↳</span>
        <span class="item-title">{{ item.title }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.backlinks-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

.backlinks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  font-size: 1rem;
}

.header-title {
  margin: 0;
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
}

.backlinks-count {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 999px;
  background: rgba(0, 229, 255, 0.15);
  color: var(--hermes-accent-blue, #00E5FF);
  border: 1px solid rgba(0, 229, 255, 0.3);
}

.backlinks-empty {
  font-size: 0.8rem;
  color: var(--hermes-text-muted);
  line-height: 1.4;
  padding: 8px 0;
}

.backlinks-empty p {
  margin: 0 0 4px 0;
}

.hint {
  font-size: 0.75rem;
  color: var(--hermes-text-muted);
  opacity: 0.8;
}

.hint code {
  color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(255, 255, 255, 0.06);
  padding: 1px 4px;
  border-radius: 4px;
}

.backlinks-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.backlink-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: var(--hermes-text-primary);
  font-size: 0.82rem;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.backlink-item:hover {
  background: rgba(0, 229, 255, 0.12);
  border-color: rgba(0, 229, 255, 0.35);
  color: var(--hermes-accent-blue, #00E5FF);
  transform: translateX(3px);
}

.item-arrow {
  color: var(--hermes-accent-pink, #FF007F);
  font-weight: 800;
}

.item-title {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

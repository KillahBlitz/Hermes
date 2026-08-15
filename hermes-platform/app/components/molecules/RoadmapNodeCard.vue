<script setup lang="ts">
import type { RoadmapNode } from '~/composables/useProgress'
import RoadmapStatusBadge from '~/components/atoms/RoadmapStatusBadge.vue'

const props = defineProps<{
  node: RoadmapNode
  isSelected?: boolean
}>()

const emit = defineEmits<{
  (e: 'select', node: RoadmapNode): void
  (e: 'openNote', node: RoadmapNode): void
  (e: 'edit', node: RoadmapNode): void
  (e: 'delete', node: RoadmapNode): void
  (e: 'startConnect', node: RoadmapNode): void
}>()
</script>

<template>
  <div
    class="roadmap-node-card glass-panel"
    :class="{ 'is-selected': isSelected, [`status-${node.status.toLowerCase()}`]: true }"
    :style="{
      left: `${node.x}px`,
      top: `${node.y}px`,
      '--node-accent': node.color || '#00E5FF'
    }"
    @click.stop="emit('select', node)"
  >
    <!-- Node Header: Icon & Status -->
    <div class="node-header">
      <span class="node-icon">{{ node.icon || '⚡' }}</span>
      <RoadmapStatusBadge :status="node.status" />
    </div>

    <!-- Node Content -->
    <div class="node-body">
      <h4 class="node-title">{{ node.title }}</h4>
      <p v-if="node.description" class="node-desc">{{ node.description }}</p>
    </div>

    <!-- Node Footer: Note Button & Connect Handle -->
    <div class="node-footer">
      <button
        type="button"
        class="note-btn"
        :class="{ 'has-note': !!node.note_id }"
        title="Abrir o crear apuntes .md de este módulo"
        @click.stop="emit('openNote', node)"
      >
        <span class="note-btn-icon">📝</span>
        <span class="note-btn-label">{{ node.note_title || 'Apuntes .md' }}</span>
      </button>

      <div class="node-actions-right">
        <button
          type="button"
          class="icon-action-btn connect-btn"
          title="Conectar a otro módulo"
          @click.stop="emit('startConnect', node)"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>

        <button
          type="button"
          class="icon-action-btn"
          title="Editar nodo"
          @click.stop="emit('edit', node)"
        >
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
        </button>

        <button
          type="button"
          class="icon-action-btn delete-icon-btn"
          title="Eliminar nodo"
          @click.stop="emit('delete', node)"
        >
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.roadmap-node-card {
  position: absolute;
  width: 260px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  cursor: grab;
  user-select: none;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
  z-index: 10;
}

.roadmap-node-card:active {
  cursor: grabbing;
}

.roadmap-node-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 3px;
  background: var(--node-accent, #00E5FF);
  border-radius: 14px 0 0 14px;
  box-shadow: 0 0 8px var(--node-accent, #00E5FF);
}

.roadmap-node-card:hover {
  border-color: rgba(0, 229, 255, 0.4);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.roadmap-node-card.is-selected {
  border-color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.3), 0 8px 24px rgba(0, 0, 0, 0.5);
}

.node-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.node-icon {
  font-size: 1.25rem;
}

.node-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.node-title {
  margin: 0;
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
  line-height: 1.3;
}

.node-desc {
  margin: 0;
  font-size: 0.76rem;
  color: var(--hermes-text-muted);
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.node-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.note-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 700;
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.25);
  color: var(--hermes-accent-blue, #00E5FF);
  cursor: pointer;
  transition: all 0.2s ease;
  max-width: 140px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.note-btn:hover {
  background: rgba(0, 229, 255, 0.2);
  border-color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
}

.node-actions-right {
  display: flex;
  align-items: center;
  gap: 4px;
}

.icon-action-btn {
  width: 24px;
  height: 24px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.icon-action-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: var(--hermes-text-primary);
}

.connect-btn:hover {
  background: rgba(0, 255, 198, 0.15);
  color: var(--hermes-accent-teal, #00FFC6);
  border-color: rgba(0, 255, 198, 0.3);
}

.delete-icon-btn:hover {
  background: rgba(255, 77, 77, 0.15);
  color: #ff4d4d;
  border-color: rgba(255, 77, 77, 0.3);
}
</style>

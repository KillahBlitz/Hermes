<script setup lang="ts">
import type { TodoSection } from '~/composables/useLists'

defineProps<{
  sections: TodoSection[]
  selectedSectionId: string
  totalPending: number
}>()

const emit = defineEmits<{
  (e: 'select', sectionId: string): void
  (e: 'newSection'): void
  (e: 'editSection', section: TodoSection): void
  (e: 'deleteSection', section: TodoSection): void
}>()
</script>

<template>
  <div class="todo-sidebar glass-panel">
    <!-- Header de Secciones -->
    <div class="sidebar-header">
      <h4 class="sidebar-title">Listas & Secciones</h4>
      <button
        type="button"
        class="add-sec-btn"
        title="Crear nueva sección"
        @click="emit('newSection')"
      >
        +
      </button>
    </div>

    <!-- Opción "Todas las Tareas" -->
    <button
      type="button"
      class="section-item-btn"
      :class="{ active: selectedSectionId === '' }"
      @click="emit('select', '')"
    >
      <div class="item-left">
        <span class="sec-icon">📋</span>
        <span class="sec-name">Todas las Tareas</span>
      </div>
      <span class="sec-counter">{{ totalPending }}</span>
    </button>

    <div class="divider"></div>

    <!-- Lista de Secciones -->
    <div class="sections-list">
      <div
        v-for="sec in sections"
        :key="sec.id"
        class="section-item-wrapper"
      >
        <button
          type="button"
          class="section-item-btn"
          :class="{ active: selectedSectionId === sec.id }"
          @click="emit('select', sec.id)"
        >
          <div class="item-left">
            <span class="sec-icon">{{ sec.icon }}</span>
            <span class="sec-name">{{ sec.name }}</span>
          </div>

          <div class="item-right">
            <span class="sec-counter" :style="{ color: sec.color }">
              {{ sec.pending_count }}
            </span>

            <div v-if="!sec.is_default" class="item-hover-actions" @click.stop>
              <button
                type="button"
                class="mini-action-btn edit"
                title="Editar sección"
                @click="emit('editSection', sec)"
              >
                ✏️
              </button>
              <button
                type="button"
                class="mini-action-btn delete"
                title="Eliminar sección"
                @click="emit('deleteSection', sec)"
              >
                ✕
              </button>
            </div>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.todo-sidebar {
  width: 240px;
  min-width: 220px;
  border-radius: 16px;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(23, 23, 28, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 6px 8px 6px;
}

.sidebar-title {
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--hermes-text-muted, #94949E);
  margin: 0;
}

.add-sec-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary, #F4F4F5);
  width: 22px;
  height: 22px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.add-sec-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.05);
  margin: 2px 0;
}

.sections-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.section-item-wrapper {
  position: relative;
}

.section-item-btn {
  width: 100%;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 8px 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
  text-align: left;
}

.section-item-btn:hover {
  background: rgba(255, 255, 255, 0.04);
  color: var(--hermes-text-primary, #F4F4F5);
}

.section-item-btn.active {
  background: rgba(0, 229, 255, 0.12);
  border-color: rgba(0, 229, 255, 0.3);
  color: var(--hermes-accent-blue, #00E5FF);
}

.item-left {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
}

.sec-icon {
  font-size: 0.95rem;
}

.sec-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-right {
  display: flex;
  align-items: center;
  gap: 6px;
}

.sec-counter {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  font-weight: 800;
  color: var(--hermes-text-muted, #94949E);
}

.section-item-btn.active .sec-counter {
  color: var(--hermes-accent-blue, #00E5FF);
}

.item-hover-actions {
  display: none;
  align-items: center;
  gap: 2px;
}

.section-item-wrapper:hover .item-hover-actions {
  display: flex;
}

.mini-action-btn {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.68rem;
  cursor: pointer;
  padding: 2px;
  border-radius: 4px;
}

.mini-action-btn:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .todo-sidebar {
    width: 100%;
  }
}
</style>

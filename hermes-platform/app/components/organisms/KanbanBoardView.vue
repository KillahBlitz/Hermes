<script setup lang="ts">
import { ref } from 'vue'
import type { Epic, KanbanBoard, Task } from '~/composables/useBoards'
import KanbanCard from '~/components/molecules/KanbanCard.vue'

defineProps<{
  kanban?: KanbanBoard | null
  epics: Epic[]
  selectedEpicId: string
  selectedTypeFilter: string
  searchQuery: string
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'updateFilters', epicId: string, typeFilter: string, search: string): void
  (e: 'moveTask', taskId: string, newStatus: 'TODO' | 'IN_PROGRESS' | 'TESTING' | 'DONE'): void
  (e: 'editTask', task: Task): void
  (e: 'deleteTask', task: Task): void
  (e: 'moveToBacklog', task: Task): void
  (e: 'newTask', statusDefault: string): void
  (e: 'openEpicManager'): void
}>()

const COLUMNS = [
  { id: 'TODO', label: 'Por Hacer', key: 'todo', color: '#FFD166', icon: '📋' },
  { id: 'IN_PROGRESS', label: 'En Progreso', key: 'in_progress', color: '#00E5FF', icon: '⚡' },
  { id: 'TESTING', label: 'Por Probar', key: 'testing', color: '#B5179E', icon: '🧪' },
  { id: 'DONE', label: 'Finalizado (< 7d)', key: 'done', color: '#00FFC6', icon: '✅' }
] as const

const draggedOverCol = ref<string | null>(null)

const handleDragOver = (e: DragEvent, colId: string) => {
  e.preventDefault()
  if (e.dataTransfer) {
    e.dataTransfer.dropEffect = 'move'
  }
  draggedOverCol.value = colId
}

const handleDragLeave = (e: DragEvent, colId: string) => {
  const currentTarget = e.currentTarget as HTMLElement
  const relatedTarget = e.relatedTarget as HTMLElement | null
  if (!currentTarget.contains(relatedTarget)) {
    if (draggedOverCol.value === colId) {
      draggedOverCol.value = null
    }
  }
}

const handleDrop = (e: DragEvent, colId: 'TODO' | 'IN_PROGRESS' | 'TESTING' | 'DONE') => {
  e.preventDefault()
  draggedOverCol.value = null
  const taskId = e.dataTransfer?.getData('text/plain')
  if (taskId) {
    emit('moveTask', taskId, colId)
  }
}
</script>

<template>
  <div class="kanban-board-view">
    <!-- Barra de Filtros y Acciones del Tablero -->
    <div class="board-filters-bar glass-panel">
      <div class="filters-left">
        <!-- Filtro Épica -->
        <select
          :value="selectedEpicId"
          class="filter-select"
          @change="emit('updateFilters', ($event.target as HTMLSelectElement).value, selectedTypeFilter, searchQuery)"
        >
          <option value="">Todas las Épicas</option>
          <option v-for="ep in epics" :key="ep.id" :value="ep.id">
            {{ ep.icon }} {{ ep.name }} ({{ ep.task_count || 0 }})
          </option>
        </select>

        <!-- Filtro Tipo -->
        <select
          :value="selectedTypeFilter"
          class="filter-select"
          @change="emit('updateFilters', selectedEpicId, ($event.target as HTMLSelectElement).value, searchQuery)"
        >
          <option value="">Todos los Tipos</option>
          <option value="IMPROVEMENT">🟢 Mejora</option>
          <option value="URGENT">🔴 Urgente</option>
          <option value="PENDING">🟡 Pendiente</option>
          <option value="ANALYSIS">🔵 Análisis</option>
        </select>

        <!-- Buscador -->
        <div class="search-wrapper">
          <span class="search-icon">🔍</span>
          <input
            :value="searchQuery"
            type="text"
            placeholder="Buscar en tareas activas..."
            class="search-input"
            @input="emit('updateFilters', selectedEpicId, selectedTypeFilter, ($event.target as HTMLInputElement).value)"
          />
        </div>
      </div>

      <div class="filters-right">
        <button class="secondary-btn" @click="emit('openEpicManager')">
          <span>💼</span> Gestionar Épicas
        </button>
        <button class="primary-btn glow-teal" @click="emit('newTask', 'TODO')">
          <span>+</span> Nueva Tarea
        </button>
      </div>
    </div>

    <!-- 4 Columnas del Tablero Kanban con Drag & Drop -->
    <div class="kanban-columns-grid">
      <div
        v-for="col in COLUMNS"
        :key="col.id"
        class="kanban-column glass-panel"
        :class="{ 'drag-over-active': draggedOverCol === col.id }"
        :style="{
          borderTopColor: col.color,
          boxShadow: draggedOverCol === col.id ? `0 0 24px ${col.color}35` : undefined
        }"
        @dragover="handleDragOver($event, col.id)"
        @dragleave="handleDragLeave($event, col.id)"
        @drop="handleDrop($event, col.id)"
      >
        <!-- Header de Columna -->
        <div class="column-header">
          <div class="col-title-group">
            <span class="col-icon">{{ col.icon }}</span>
            <span class="col-title">{{ col.label }}</span>
            <span
              class="col-counter"
              :style="{ color: col.color, backgroundColor: `${col.color}15` }"
            >
              {{ kanban ? (kanban[col.key]?.length || 0) : 0 }}
            </span>
          </div>

          <button
            class="col-add-btn"
            title="Añadir tarea a esta columna"
            @click="emit('newTask', col.id)"
          >
            +
          </button>
        </div>

        <!-- Lista de Tarjetas -->
        <div class="cards-stack">
          <div v-if="loading" class="col-skeleton shimmer"></div>

          <template v-else-if="kanban && kanban[col.key]?.length > 0">
            <KanbanCard
              v-for="task in kanban[col.key]"
              :key="task.id"
              :task="task"
              @move="emit('moveTask', task.id, $event)"
              @edit="emit('editTask', task)"
              @delete="emit('deleteTask', task)"
              @move-to-backlog="emit('moveToBacklog', task)"
            />
          </template>

          <div v-else class="col-empty-placeholder">
            <span>Sin tareas</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.kanban-board-view {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.board-filters-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  border-radius: 14px;
  flex-wrap: wrap;
  gap: 12px;
}

.filters-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  flex-wrap: wrap;
}

.filter-select {
  background: rgba(23, 23, 28, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary, #F4F4F5);
  padding: 7px 12px;
  border-radius: 10px;
  font-size: 0.82rem;
  font-weight: 500;
  outline: none;
}

.filter-select option {
  background: #17171c;
  color: #F4F4F5;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 180px;
}

.search-icon {
  position: absolute;
  left: 10px;
  font-size: 0.78rem;
  opacity: 0.6;
  pointer-events: none;
}

.search-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 7px 12px 7px 30px;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.82rem;
  outline: none;
}

.filters-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.primary-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  font-weight: 800;
  font-size: 0.85rem;
  padding: 8px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 16px rgba(0, 255, 198, 0.4);
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-primary, #F4F4F5);
  font-weight: 600;
  font-size: 0.85rem;
  padding: 8px 14px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

/* Cuadrícula de 4 Columnas */
.kanban-columns-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  align-items: start;
}

.kanban-column {
  border-radius: 14px;
  border-top: 3px solid;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 480px;
  background: rgba(23, 23, 28, 0.7);
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.kanban-column.drag-over-active {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.01);
}

.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.col-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.col-icon { font-size: 0.95rem; }

.col-title {
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  letter-spacing: 0.02em;
}

.col-counter {
  font-size: 0.72rem;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 6px;
  font-family: 'JetBrains Mono', monospace;
}

.col-add-btn {
  background: rgba(255, 255, 255, 0.05);
  border: none;
  color: var(--hermes-text-muted, #94949E);
  width: 24px;
  height: 24px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.9rem;
  transition: all 0.15s ease;
}

.col-add-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.cards-stack {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.col-empty-placeholder {
  padding: 30px 10px;
  text-align: center;
  font-size: 0.78rem;
  color: var(--hermes-text-muted, #94949E);
  opacity: 0.5;
  border: 1px dashed rgba(255, 255, 255, 0.08);
  border-radius: 10px;
}

.col-skeleton {
  height: 90px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
}

.shimmer {
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.02) 25%, rgba(255, 255, 255, 0.06) 50%, rgba(255, 255, 255, 0.02) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.6s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

@media (max-width: 1100px) {
  .kanban-columns-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .kanban-columns-grid {
    grid-template-columns: 1fr;
  }
}
</style>

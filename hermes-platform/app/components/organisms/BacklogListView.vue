<script setup lang="ts">
import type { Epic, Task } from '~/composables/useBoards'
import KanbanCard from '~/components/molecules/KanbanCard.vue'

defineProps<{
  tasks: Task[]
  epics: Epic[]
  selectedEpicId: string
  selectedTypeFilter: string
  searchQuery: string
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'updateFilters', epicId: string, typeFilter: string, search: string): void
  (e: 'moveToBoard', task: Task): void
  (e: 'editTask', task: Task): void
  (e: 'deleteTask', task: Task): void
  (e: 'newTask'): void
}>()
</script>

<template>
  <div class="backlog-view glass-panel">
    <!-- Header & Filtros -->
    <div class="backlog-header">
      <div class="header-info">
        <h3 class="section-title">Backlog de Tareas</h3>
        <span class="count-badge">{{ tasks.length }} tareas en espera</span>
      </div>

      <div class="filters-actions-bar">
        <select
          :value="selectedEpicId"
          class="filter-select"
          @change="emit('updateFilters', ($event.target as HTMLSelectElement).value, selectedTypeFilter, searchQuery)"
        >
          <option value="">Todas las Épicas</option>
          <option v-for="ep in epics" :key="ep.id" :value="ep.id">
            {{ ep.icon }} {{ ep.name }}
          </option>
        </select>

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

        <input
          :value="searchQuery"
          type="text"
          placeholder="Buscar en Backlog..."
          class="search-input"
          @input="emit('updateFilters', selectedEpicId, selectedTypeFilter, ($event.target as HTMLInputElement).value)"
        />

        <button class="primary-btn glow-teal" @click="emit('newTask')">
          <span>+</span> Tarea al Backlog
        </button>
      </div>
    </div>

    <!-- Lista de Tareas en Backlog -->
    <div class="backlog-content">
      <div v-if="loading" class="skeletons-list">
        <div v-for="i in 3" :key="i" class="row-skeleton shimmer"></div>
      </div>

      <div v-else-if="tasks.length === 0" class="empty-state">
        <span class="empty-icon">📥</span>
        <h4 class="empty-title">El Backlog está vacío</h4>
        <p class="empty-desc">No hay tareas pendientes en la cola. Agrega tareas para priorizarlas antes de enviarlas al tablero Kanban.</p>
        <button class="primary-btn glow-teal sm" @click="emit('newTask')">
          + Crear primera tarea en Backlog
        </button>
      </div>

      <div v-else class="tasks-grid">
        <KanbanCard
          v-for="task in tasks"
          :key="task.id"
          :task="task"
          @edit="emit('editTask', task)"
          @delete="emit('deleteTask', task)"
          @move-to-board="emit('moveToBoard', task)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.backlog-view {
  padding: 22px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.backlog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 14px;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
}

.count-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--hermes-text-muted, #94949E);
}

.filters-actions-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-select {
  background: rgba(23, 23, 28, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary, #F4F4F5);
  padding: 7px 12px;
  border-radius: 10px;
  font-size: 0.82rem;
  outline: none;
}

.filter-select option {
  background: #17171c;
  color: #F4F4F5;
}

.search-input {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 7px 12px;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.82rem;
  outline: none;
  min-width: 180px;
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

.primary-btn.sm {
  font-size: 0.8rem;
  padding: 6px 12px;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 16px rgba(0, 255, 198, 0.4);
}

.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}

.skeletons-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}

.row-skeleton {
  height: 120px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
}

.shimmer {
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.02) 25%, rgba(255, 255, 255, 0.06) 50%, rgba(255, 255, 255, 0.02) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.6s infinite;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 2.2rem;
  margin-bottom: 10px;
  opacity: 0.7;
}

.empty-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--hermes-text-primary, #F4F4F5);
  margin-bottom: 6px;
}

.empty-desc {
  font-size: 0.82rem;
  color: var(--hermes-text-muted, #94949E);
  margin-bottom: 16px;
  max-width: 360px;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
</style>

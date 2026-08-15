<script setup lang="ts">
import type { Epic, Task } from '~/composables/useBoards'
import KanbanCard from '~/components/molecules/KanbanCard.vue'

defineProps<{
  tasks: Task[]
  epics: Epic[]
  selectedEpicId: string
  searchQuery: string
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'updateFilters', epicId: string, search: string): void
  (e: 'editTask', task: Task): void
  (e: 'deleteTask', task: Task): void
}>()
</script>

<template>
  <div class="archived-view glass-panel">
    <!-- Header Informativo -->
    <div class="archived-header">
      <div class="header-info">
        <h3 class="section-title">Tareas Finalizadas (+7 días)</h3>
        <span class="count-badge">{{ tasks.length }} archivadas</span>
      </div>

      <div class="filters-bar">
        <select
          :value="selectedEpicId"
          class="filter-select"
          @change="emit('updateFilters', ($event.target as HTMLSelectElement).value, searchQuery)"
        >
          <option value="">Todas las Épicas</option>
          <option v-for="ep in epics" :key="ep.id" :value="ep.id">
            {{ ep.icon }} {{ ep.name }}
          </option>
        </select>

        <input
          :value="searchQuery"
          type="text"
          placeholder="Buscar en histórico..."
          class="search-input"
          @input="emit('updateFilters', selectedEpicId, ($event.target as HTMLInputElement).value)"
        />
      </div>
    </div>

    <!-- Banner Explicativo -->
    <div class="info-notice">
      <span>ℹ️</span>
      <p>Las tareas completadas hace más de 7 días se trasladan automáticamente a este archivo para mantener el tablero Kanban ágil y enfocado.</p>
    </div>

    <!-- Lista de Tareas Archivadas -->
    <div class="archived-content">
      <div v-if="loading" class="skeletons-list">
        <div v-for="i in 3" :key="i" class="row-skeleton shimmer"></div>
      </div>

      <div v-else-if="tasks.length === 0" class="empty-state">
        <span class="empty-icon">🗄️</span>
        <h4 class="empty-title">Sin tareas archivadas</h4>
        <p class="empty-desc">Las tareas completadas que superen los 7 días de antigüedad aparecerán aquí.</p>
      </div>

      <div v-else class="tasks-grid">
        <KanbanCard
          v-for="task in tasks"
          :key="task.id"
          :task="task"
          :is-archived="true"
          @edit="emit('editTask', task)"
          @delete="emit('deleteTask', task)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.archived-view {
  padding: 22px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.archived-header {
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
  background: rgba(0, 255, 198, 0.08);
  color: var(--hermes-accent-teal, #00FFC6);
  border: 1px solid rgba(0, 255, 198, 0.2);
}

.filters-bar {
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

.info-notice {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 10px;
  background: rgba(0, 229, 255, 0.04);
  border: 1px solid rgba(0, 229, 255, 0.15);
  font-size: 0.8rem;
  color: var(--hermes-text-muted, #94949E);
}

.info-notice p {
  margin: 0;
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
  max-width: 360px;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
</style>

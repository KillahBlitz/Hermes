<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Task } from '~/composables/useBoards'
import TaskTypeBadge from '~/components/atoms/TaskTypeBadge.vue'
import ComplexityPill from '~/components/atoms/ComplexityPill.vue'
import EpicBadge from '~/components/atoms/EpicBadge.vue'

const props = defineProps<{
  task: Task
  isArchived?: boolean
}>()

const emit = defineEmits<{
  (e: 'move', status: 'TODO' | 'IN_PROGRESS' | 'TESTING' | 'DONE'): void
  (e: 'edit', task: Task): void
  (e: 'delete', task: Task): void
  (e: 'moveToBacklog', task: Task): void
  (e: 'moveToBoard', task: Task): void
}>()

const showStatusMenu = ref(false)
const isDragging = ref(false)

const handleDragStart = (e: DragEvent) => {
  if (!e.dataTransfer) return
  isDragging.value = true
  e.dataTransfer.setData('text/plain', props.task.id)
  e.dataTransfer.effectAllowed = 'move'
}

const handleDragEnd = () => {
  isDragging.value = false
}

const formattedDueDate = computed(() => {
  if (!props.task.due_date) return null
  const d = new Date(props.task.due_date)
  return new Intl.DateTimeFormat('es-MX', { day: '2-digit', month: 'short' }).format(d)
})

const isOverdue = computed(() => {
  if (!props.task.due_date || props.task.status === 'DONE') return false
  return new Date(props.task.due_date) < new Date()
})

const statusOptions: Array<{ id: 'TODO' | 'IN_PROGRESS' | 'TESTING' | 'DONE'; label: string; icon: string }> = [
  { id: 'TODO', label: 'Por Hacer (ToDo)', icon: '📋' },
  { id: 'IN_PROGRESS', label: 'En Progreso', icon: '⚡' },
  { id: 'TESTING', label: 'Por Probar (Testing)', icon: '🧪' },
  { id: 'DONE', label: 'Finalizado (Done)', icon: '✅' }
]
</script>

<template>
  <div
    class="kanban-card glass-panel"
    :class="[task.type.toLowerCase(), { 'is-overdue': isOverdue, 'is-dragging': isDragging }]"
    :draggable="!isArchived"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
  >
    <!-- Top Row: Badges -->
    <div class="card-badges-row">
      <div class="left-badges">
        <EpicBadge
          v-if="task.epic"
          :name="task.epic.name"
          :icon="task.epic.icon"
          :color="task.epic.color"
          size="sm"
        />
        <TaskTypeBadge :type="task.type" size="sm" />
      </div>

      <ComplexityPill :complexity="task.complexity" size="sm" />
    </div>

    <!-- Title & Description -->
    <div class="card-content-box">
      <h4 class="task-title" :title="task.title">{{ task.title }}</h4>
      <p v-if="task.description" class="task-desc-snippet" :title="task.description">
        {{ task.description }}
      </p>
    </div>

    <!-- Meta: Fechas y Días Finalizados -->
    <div v-if="task.due_date || (task.status === 'DONE' && task.days_since_completion !== undefined)" class="card-meta-row">
      <span v-if="formattedDueDate" class="due-date-badge" :class="{ 'overdue': isOverdue }">
        📅 {{ formattedDueDate }}
      </span>

      <span v-if="task.status === 'DONE' && task.days_since_completion !== undefined" class="done-days-badge">
        ✨ Hace {{ task.days_since_completion }}d
      </span>
    </div>

    <!-- Bottom Actions -->
    <div class="card-footer">
      <!-- Selector Rápido de Estado / Columna -->
      <div v-if="!isArchived && task.location === 'BOARD'" class="status-dropdown-wrapper">
        <button
          class="status-pill-btn"
          @click.stop="showStatusMenu = !showStatusMenu"
        >
          <span class="status-dot" :class="task.status.toLowerCase()"></span>
          <span>Mover</span>
          <span class="arrow-small">▼</span>
        </button>

        <div v-if="showStatusMenu" class="status-menu glass-panel" @click.stop>
          <button
            v-for="opt in statusOptions"
            :key="opt.id"
            class="status-menu-item"
            :class="{ active: task.status === opt.id }"
            @click="emit('move', opt.id); showStatusMenu = false"
          >
            <span>{{ opt.icon }}</span>
            <span>{{ opt.label }}</span>
          </button>
        </div>
      </div>

      <!-- Botón mover a tablero si está en Backlog -->
      <button
        v-if="task.location === 'BACKLOG'"
        class="move-board-btn glow-teal"
        title="Pasar al tablero Kanban activo"
        @click="emit('moveToBoard', task)"
      >
        <span>+ Tablero</span>
      </button>

      <!-- Botones de Edición / Borrado -->
      <div class="right-actions">
        <button
          v-if="task.location === 'BOARD' && !isArchived"
          class="icon-action-btn"
          title="Mover a Backlog"
          @click="emit('moveToBacklog', task)"
        >
          📥
        </button>
        <button
          class="icon-action-btn edit"
          title="Editar tarea"
          @click="emit('edit', task)"
        >
          ✏️
        </button>
        <button
          class="icon-action-btn delete"
          title="Eliminar tarea"
          @click="emit('delete', task)"
        >
          🗑️
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.kanban-card {
  border-radius: 12px;
  padding: 14px;
  background: rgba(23, 23, 28, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: relative;
  transition: transform 0.2s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.2s ease, border-color 0.2s ease;
  user-select: none;
}

.kanban-card:hover {
  transform: translateY(-2px);
  background: rgba(23, 23, 28, 0.98);
  border-color: rgba(255, 255, 255, 0.16);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}

.kanban-card.is-dragging {
  opacity: 0.45;
  cursor: grabbing;
  transform: scale(0.98);
  border-style: dashed;
}

.kanban-card.improvement:hover { border-left: 3px solid #00FFC6; }
.kanban-card.urgent:hover { border-left: 3px solid #FF007F; }
.kanban-card.pending:hover { border-left: 3px solid #FFD166; }
.kanban-card.analysis:hover { border-left: 3px solid #00E5FF; }

.card-badges-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  flex-wrap: wrap;
}

.left-badges {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.card-content-box {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.task-title {
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
  line-height: 1.3;
}

.task-desc-snippet {
  font-size: 0.78rem;
  color: var(--hermes-text-muted, #94949E);
  margin: 0;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.72rem;
}

.due-date-badge {
  color: var(--hermes-text-muted, #94949E);
  background: rgba(255, 255, 255, 0.04);
  padding: 2px 6px;
  border-radius: 4px;
}

.due-date-badge.overdue {
  color: var(--hermes-accent-pink, #FF007F);
  background: rgba(255, 0, 127, 0.12);
  font-weight: 700;
}

.done-days-badge {
  color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.08);
  padding: 2px 6px;
  border-radius: 4px;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.status-dropdown-wrapper {
  position: relative;
}

.status-pill-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted, #94949E);
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.status-pill-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-primary, #F4F4F5);
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.status-dot.todo { background: #FFD166; }
.status-dot.in_progress { background: #00E5FF; }
.status-dot.testing { background: #B5179E; }
.status-dot.done { background: #00FFC6; }

.arrow-small {
  font-size: 0.55rem;
  opacity: 0.6;
}

.status-menu {
  position: absolute;
  bottom: calc(100% + 4px);
  left: 0;
  z-index: 40;
  width: 180px;
  background: rgba(23, 23, 28, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  padding: 4px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.status-menu-item {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted, #94949E);
  padding: 6px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s ease;
}

.status-menu-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary, #F4F4F5);
}

.status-menu-item.active {
  background: rgba(0, 229, 255, 0.12);
  color: var(--hermes-accent-blue, #00E5FF);
}

.move-board-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  font-size: 0.72rem;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 6px;
  cursor: pointer;
}

.right-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.kanban-card:hover .right-actions {
  opacity: 1;
}

.icon-action-btn {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted, #94949E);
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.icon-action-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}
</style>

<script setup lang="ts">
import { computed } from 'vue'
import type { TodoTask } from '~/composables/useLists'
import DifficultyPointsPill from '~/components/atoms/DifficultyPointsPill.vue'

const props = defineProps<{
  task: TodoTask
}>()

const emit = defineEmits<{
  (e: 'toggle', task: TodoTask): void
  (e: 'edit', task: TodoTask): void
  (e: 'delete', task: TodoTask): void
}>()

const formattedDueDate = computed(() => {
  if (!props.task.due_date) return null
  const d = new Date(props.task.due_date)
  return new Intl.DateTimeFormat('es-MX', { day: '2-digit', month: 'short' }).format(d)
})

const isOverdue = computed(() => {
  if (!props.task.due_date || props.task.is_completed) return false
  return new Date(props.task.due_date) < new Date()
})

const repeatLabel = computed(() => {
  switch (props.task.repeat) {
    case 'DAILY': return 'Diaria'
    case 'WEEKDAYS': return 'L-V'
    case 'WEEKLY': return 'Semanal'
    case 'MONTHLY': return 'Mensual'
    default: return null
  }
})
</script>

<template>
  <div
    class="todo-task-row glass-panel"
    :class="{ 'is-completed': task.is_completed, 'is-overdue': isOverdue }"
    @click="emit('edit', task)"
  >
    <!-- Checkbox Circular -->
    <button
      type="button"
      class="round-checkbox-btn"
      :class="{ checked: task.is_completed }"
      :title="task.is_completed ? 'Marcar como pendiente' : 'Marcar como completada'"
      @click.stop="emit('toggle', task)"
    >
      <span v-if="task.is_completed" class="check-icon">✓</span>
    </button>

    <!-- Contenido de la Tarea -->
    <div class="task-info-block">
      <div class="task-title-line">
        <span class="task-title" :class="{ strike: task.is_completed }">
          {{ task.title }}
        </span>
      </div>

      <!-- Metadatos de la Tarea -->
      <div class="task-meta-line">
        <!-- Sección Badge -->
        <span
          v-if="task.section"
          class="section-tag"
          :style="{
            color: task.section.color,
            borderColor: `${task.section.color}35`,
            backgroundColor: `${task.section.color}12`
          }"
        >
          <span>{{ task.section.icon }}</span>
          <span>{{ task.section.name }}</span>
        </span>

        <!-- Puntos de Dificultad -->
        <DifficultyPointsPill :points="task.difficulty_points" size="sm" />

        <!-- Repetición -->
        <span v-if="repeatLabel" class="repeat-tag" title="Frecuencia de repetición">
          🔁 {{ repeatLabel }}
        </span>

        <!-- Fecha Límite -->
        <span v-if="formattedDueDate" class="due-tag" :class="{ overdue: isOverdue }">
          📅 {{ formattedDueDate }}
        </span>

        <!-- Indicador de Notas -->
        <span v-if="task.notes" class="notes-icon" title="Contiene notas o pasos">
          📝
        </span>
      </div>
    </div>

    <!-- Acciones Rápidas -->
    <div class="row-actions" @click.stop>
      <button
        type="button"
        class="action-btn edit"
        title="Editar tarea"
        @click="emit('edit', task)"
      >
        ✏️
      </button>

      <button
        type="button"
        class="action-btn delete"
        title="Eliminar tarea"
        @click="emit('delete', task)"
      >
        🗑️
      </button>
    </div>
  </div>
</template>

<style scoped>
.todo-task-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 16px;
  border-radius: 12px;
  background: rgba(23, 23, 28, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.06);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
  user-select: none;
}

.todo-task-row:hover {
  background: rgba(23, 23, 28, 0.95);
  border-color: rgba(255, 255, 255, 0.14);
  transform: translateX(2px);
}

.todo-task-row.is-completed {
  opacity: 0.6;
  background: rgba(23, 23, 28, 0.4);
}

.todo-task-row.is-completed:hover {
  opacity: 0.85;
}

/* Checkbox circular */
.round-checkbox-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.25);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
  padding: 0;
}

.round-checkbox-btn:hover {
  border-color: var(--hermes-accent-teal, #00FFC6);
  transform: scale(1.1);
}

.round-checkbox-btn.checked {
  background: var(--hermes-accent-teal, #00FFC6);
  border-color: var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 0 10px rgba(0, 255, 198, 0.4);
}

.check-icon {
  color: #0c0c0e;
  font-size: 0.8rem;
  font-weight: 900;
}

/* Info */
.task-info-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  overflow: hidden;
}

.task-title-line {
  display: flex;
  align-items: center;
}

.task-title {
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--hermes-text-primary, #F4F4F5);
  line-height: 1.3;
  transition: color 0.2s ease;
}

.task-title.strike {
  text-decoration: line-through;
  color: var(--hermes-text-muted, #94949E);
}

.task-meta-line {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.section-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 6px;
  border: 1px solid;
}

.repeat-tag {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--hermes-text-muted, #94949E);
  background: rgba(255, 255, 255, 0.04);
  padding: 1px 6px;
  border-radius: 6px;
}

.due-tag {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--hermes-text-muted, #94949E);
  background: rgba(255, 255, 255, 0.04);
  padding: 1px 6px;
  border-radius: 6px;
}

.due-tag.overdue {
  color: var(--hermes-accent-pink, #FF007F);
  background: rgba(255, 0, 127, 0.12);
  font-weight: 700;
}

.notes-icon {
  font-size: 0.75rem;
  opacity: 0.7;
}

/* Actions */
.row-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.todo-task-row:hover .row-actions {
  opacity: 1;
}

.action-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted, #94949E);
  width: 26px;
  height: 26px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}
</style>

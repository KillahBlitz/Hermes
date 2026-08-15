<script setup lang="ts">
import type { Habit } from '~/composables/useBoards'
import HabitDayBox from '~/components/atoms/HabitDayBox.vue'

const props = defineProps<{
  habit: Habit
}>()

const emit = defineEmits<{
  (e: 'checkDay', habitId: string, dayNumber: number, newStatus: 'COMPLETED' | 'FAILED' | 'PENDING'): void
  (e: 'edit', habit: Habit): void
  (e: 'delete', habit: Habit): void
}>()

const handleDayClick = (dayNumber: number, currentStatus: 'COMPLETED' | 'FAILED' | 'PENDING') => {
  let nextStatus: 'COMPLETED' | 'FAILED' | 'PENDING' = 'COMPLETED'
  if (currentStatus === 'COMPLETED') nextStatus = 'FAILED'
  else if (currentStatus === 'FAILED') nextStatus = 'PENDING'
  else nextStatus = 'COMPLETED'

  emit('checkDay', props.habit.id, dayNumber, nextStatus)
}
</script>

<template>
  <div class="habit-card glass-panel" :class="{ 'is-consolidated': habit.is_consolidated }">
    <!-- Header del Hábito -->
    <div class="habit-header">
      <div class="habit-title-box">
        <div
          class="habit-icon-avatar"
          :style="{
            color: habit.color || '#00FFC6',
            backgroundColor: `${habit.color || '#00FFC6'}18`,
            borderColor: `${habit.color || '#00FFC6'}40`
          }"
        >
          {{ habit.icon || '⚡' }}
        </div>

        <div class="habit-titles">
          <h3 class="habit-title">{{ habit.title }}</h3>
          <p v-if="habit.description" class="habit-desc">{{ habit.description }}</p>
        </div>
      </div>

      <!-- Badges de Racha y Acciones -->
      <div class="habit-top-right">
        <div v-if="habit.is_consolidated" class="consolidated-badge">
          🏆 Consolidado (21/21)
        </div>
        <div v-else class="streak-badge">
          🔥 {{ habit.current_streak }} días seguidos
        </div>

        <div class="habit-actions">
          <button class="action-btn edit" title="Editar hábito" @click="emit('edit', habit)">
            ✏️
          </button>
          <button class="action-btn delete" title="Eliminar hábito" @click="emit('delete', habit)">
            🗑️
          </button>
        </div>
      </div>
    </div>

    <!-- Barra de Progreso hacia los 21 Días -->
    <div class="progress-section">
      <div class="progress-labels">
        <span class="progress-count">{{ habit.total_completed }} de 21 días completados</span>
        <span class="progress-pct">{{ habit.completion_percentage }}%</span>
      </div>

      <div class="progress-track">
        <div
          class="progress-fill"
          :style="{
            width: `${habit.completion_percentage}%`,
            backgroundColor: habit.color || '#00FFC6',
            boxShadow: `0 0 10px ${habit.color || '#00FFC6'}40`
          }"
        ></div>
      </div>
    </div>

    <!-- Matriz de las 21 Casillas -->
    <div class="days-matrix-wrapper">
      <span class="matrix-instruction">Haz clic en cada día para marcar: ✓ Cumplido | ✕ Fallido | • Pendiente</span>
      <div class="days-grid">
        <HabitDayBox
          v-for="d in habit.days"
          :key="d.day_number"
          :day-number="d.day_number"
          :status="d.status"
          :date="d.date"
          @click="handleDayClick(d.day_number, d.status)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.habit-card {
  padding: 22px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: rgba(23, 23, 28, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.habit-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.16);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
}

.habit-card.is-consolidated {
  border-color: rgba(255, 209, 102, 0.4);
  box-shadow: 0 0 24px rgba(255, 209, 102, 0.15);
}

.habit-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
}

.habit-title-box {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 200px;
}

.habit-icon-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  flex-shrink: 0;
}

.habit-titles {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.habit-title {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
}

.habit-desc {
  font-size: 0.8rem;
  color: var(--hermes-text-muted, #94949E);
  margin: 0;
}

.habit-top-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.streak-badge {
  font-size: 0.78rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 8px;
  background: rgba(255, 209, 102, 0.12);
  color: #FFD166;
  border: 1px solid rgba(255, 209, 102, 0.3);
}

.consolidated-badge {
  font-size: 0.78rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(255, 209, 102, 0.2), rgba(0, 255, 198, 0.2));
  color: #FFD166;
  border: 1px solid rgba(255, 209, 102, 0.5);
  box-shadow: 0 0 12px rgba(255, 209, 102, 0.2);
}

.habit-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.action-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted, #94949E);
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

/* Progreso */
.progress-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.progress-labels {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.75rem;
  color: var(--hermes-text-muted, #94949E);
}

.progress-pct {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
}

.progress-track {
  height: 6px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.06);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}

/* Matriz */
.days-matrix-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.matrix-instruction {
  font-size: 0.7rem;
  color: var(--hermes-text-muted, #94949E);
  opacity: 0.7;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(36px, 1fr));
  gap: 6px;
}
</style>

<script setup lang="ts">
import type { Habit } from '~/composables/useBoards'
import HabitCard from '~/components/molecules/HabitCard.vue'

defineProps<{
  habits: Habit[]
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'checkDay', habitId: string, dayNumber: number, newStatus: 'COMPLETED' | 'FAILED' | 'PENDING'): void
  (e: 'editHabit', habit: Habit): void
  (e: 'deleteHabit', habit: Habit): void
  (e: 'newHabit'): void
}>()
</script>

<template>
  <div class="habits-board-view">
    <!-- Header de Hábitos -->
    <div class="habits-top-bar glass-panel">
      <div class="top-bar-info">
        <h2 class="habits-section-title">Método 21 Días: Construcción de Hábitos</h2>
        <p class="habits-section-desc">
          La neurociencia demuestra que se requieren 21 días de práctica consecutiva para consolidar una nueva ruta neuronal.
        </p>
      </div>

      <div class="top-bar-actions">
        <button class="primary-btn glow-teal" @click="emit('newHabit')">
          <span>+</span> Nuevo Hábito
        </button>
      </div>
    </div>

    <!-- Lista de Hábitos -->
    <div class="habits-grid-container">
      <div v-if="loading" class="skeletons-list">
        <div v-for="i in 2" :key="i" class="habit-skeleton shimmer"></div>
      </div>

      <div v-else-if="habits.length === 0" class="empty-state glass-panel">
        <span class="empty-icon">⚡</span>
        <h3 class="empty-title">Sin hábitos activos</h3>
        <p class="empty-desc">
          Empieza registrando tu primer hábito diario (ej. "Lectura 20 min", "Ejercicio matutino", "Meditación") para comenzar el reto de 21 días.
        </p>
        <button class="primary-btn glow-teal" @click="emit('newHabit')">
          + Crear mi primer hábito
        </button>
      </div>

      <div v-else class="habits-cards-list">
        <HabitCard
          v-for="habit in habits"
          :key="habit.id"
          :habit="habit"
          @check-day="(hId, day, st) => emit('checkDay', hId, day, st)"
          @edit="emit('editHabit', habit)"
          @delete="emit('deleteHabit', habit)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.habits-board-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.habits-top-bar {
  padding: 20px 24px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.habits-section-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0 0 4px 0;
}

.habits-section-desc {
  font-size: 0.85rem;
  color: var(--hermes-text-muted, #94949E);
  margin: 0;
  max-width: 600px;
}

.primary-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  font-weight: 800;
  font-size: 0.9rem;
  padding: 10px 18px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 20px rgba(0, 255, 198, 0.4);
}

.habits-cards-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skeletons-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.habit-skeleton {
  height: 200px;
  border-radius: 16px;
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
  padding: 60px 24px;
  text-align: center;
  border-radius: 16px;
}

.empty-icon {
  font-size: 2.8rem;
  margin-bottom: 12px;
  color: var(--hermes-accent-teal, #00FFC6);
}

.empty-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 0.88rem;
  color: var(--hermes-text-muted, #94949E);
  max-width: 440px;
  margin-bottom: 20px;
  line-height: 1.5;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
</style>

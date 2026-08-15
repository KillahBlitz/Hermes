<script setup lang="ts">
const props = defineProps<{
  dayNumber: number
  status: 'COMPLETED' | 'FAILED' | 'PENDING'
  date?: string
}>()

const emit = defineEmits<{
  (e: 'click'): void
}>()
</script>

<template>
  <button
    type="button"
    class="habit-day-box"
    :class="status.toLowerCase()"
    :title="`Día ${dayNumber}: ${status === 'COMPLETED' ? 'Completado' : status === 'FAILED' ? 'Fallido' : 'Pendiente'}`"
    @click="emit('click')"
  >
    <span class="day-num">D{{ dayNumber }}</span>
    <span class="day-status-icon">
      <template v-if="status === 'COMPLETED'">✓</template>
      <template v-else-if="status === 'FAILED'">✕</template>
      <template v-else>•</template>
    </span>
  </button>
</template>

<style scoped>
.habit-day-box {
  width: 38px;
  height: 44px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.03);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
  padding: 0;
}

.habit-day-box:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.day-num {
  font-size: 0.65rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  color: var(--hermes-text-muted, #94949E);
  line-height: 1;
}

.day-status-icon {
  font-size: 0.85rem;
  font-weight: 900;
  line-height: 1;
  color: var(--hermes-text-muted, #94949E);
}

/* Completado */
.habit-day-box.completed {
  background: rgba(0, 255, 198, 0.15);
  border-color: var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 0 12px rgba(0, 255, 198, 0.25);
}

.habit-day-box.completed .day-num {
  color: var(--hermes-accent-teal, #00FFC6);
}

.habit-day-box.completed .day-status-icon {
  color: var(--hermes-accent-teal, #00FFC6);
  text-shadow: 0 0 8px var(--hermes-accent-teal, #00FFC6);
}

/* Fallido */
.habit-day-box.failed {
  background: rgba(255, 0, 127, 0.12);
  border-color: var(--hermes-accent-pink, #FF007F);
}

.habit-day-box.failed .day-num,
.habit-day-box.failed .day-status-icon {
  color: var(--hermes-accent-pink, #FF007F);
}

/* Pendiente */
.habit-day-box.pending:hover {
  background: rgba(0, 229, 255, 0.08);
  border-color: var(--hermes-accent-blue, #00E5FF);
}
</style>

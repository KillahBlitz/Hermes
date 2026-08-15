<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  daysRemaining: number
  isOverdue: boolean
  isCompleted?: boolean
}>()

const badgeText = computed(() => {
  if (props.isCompleted) return '¡Completado! 🎉'
  if (props.isOverdue) {
    const days = Math.abs(props.daysRemaining)
    return `Vencido (+${days}d)`
  }
  if (props.daysRemaining === 0) return '¡Vence hoy! ⏳'
  if (props.daysRemaining === 1) return '1 día restante'
  return `${props.daysRemaining} días restantes`
})

const badgeClass = computed(() => {
  if (props.isCompleted) return 'badge-completed'
  if (props.isOverdue) return 'badge-overdue'
  if (props.daysRemaining <= 7) return 'badge-urgent'
  if (props.daysRemaining <= 30) return 'badge-medium'
  return 'badge-normal'
})
</script>

<template>
  <div class="countdown-badge" :class="badgeClass">
    <span class="badge-dot" />
    <span class="badge-text">{{ badgeText }}</span>
  </div>
</template>

<style scoped>
.countdown-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  transition: all 0.25s ease;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

/* Completed */
.badge-completed {
  background: rgba(0, 255, 198, 0.12);
  color: var(--hermes-accent-teal, #00FFC6);
  border: 1px solid rgba(0, 255, 198, 0.3);
}
.badge-completed .badge-dot {
  background: var(--hermes-accent-teal, #00FFC6);
}

/* Overdue */
.badge-overdue {
  background: rgba(255, 77, 77, 0.12);
  color: #ff4d4d;
  border: 1px solid rgba(255, 77, 77, 0.3);
}
.badge-overdue .badge-dot {
  background: #ff4d4d;
}

/* Urgent < 7 days */
.badge-urgent {
  background: rgba(255, 0, 127, 0.12);
  color: var(--hermes-accent-pink, #FF007F);
  border: 1px solid rgba(255, 0, 127, 0.35);
  box-shadow: 0 0 10px rgba(255, 0, 127, 0.2);
  animation: pulse-glow 2s infinite ease-in-out;
}
.badge-urgent .badge-dot {
  background: var(--hermes-accent-pink, #FF007F);
}

/* Medium 8-30 days */
.badge-medium {
  background: rgba(255, 209, 102, 0.12);
  color: #ffd166;
  border: 1px solid rgba(255, 209, 102, 0.3);
}
.badge-medium .badge-dot {
  background: #ffd166;
}

/* Normal > 30 days */
.badge-normal {
  background: rgba(0, 229, 255, 0.12);
  color: var(--hermes-accent-blue, #00E5FF);
  border: 1px solid rgba(0, 229, 255, 0.25);
}
.badge-normal .badge-dot {
  background: var(--hermes-accent-blue, #00E5FF);
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 8px rgba(255, 0, 127, 0.15);
  }
  50% {
    box-shadow: 0 0 16px rgba(255, 0, 127, 0.35);
  }
}
</style>

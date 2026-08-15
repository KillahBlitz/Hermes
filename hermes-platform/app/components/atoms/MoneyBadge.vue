<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    amount: number
    type?: 'INCOME' | 'EXPENSE' | 'NEUTRAL'
    size?: 'sm' | 'md' | 'lg' | 'xl'
    showSign?: boolean
  }>(),
  {
    type: 'NEUTRAL',
    size: 'md',
    showSign: true
  }
)

const formattedValue = computed(() => {
  const abs = Math.abs(props.amount)
  const formatted = new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'MXN',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(abs)

  if (!props.showSign || props.type === 'NEUTRAL') {
    return formatted
  }
  return props.type === 'INCOME' ? `+${formatted}` : `-${formatted}`
})
</script>

<template>
  <span class="money-badge" :class="[type.toLowerCase(), size]">
    {{ formattedValue }}
  </span>
</template>

<style scoped>
.money-badge {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  letter-spacing: -0.02em;
  display: inline-flex;
  align-items: center;
  border-radius: 6px;
  transition: all 0.2s ease;
}

/* Tipos */
.money-badge.income {
  color: var(--hermes-accent-teal, #00FFC6);
  text-shadow: 0 0 12px rgba(0, 255, 198, 0.35);
}

.money-badge.expense {
  color: var(--hermes-accent-pink, #FF007F);
  text-shadow: 0 0 12px rgba(255, 0, 127, 0.35);
}

.money-badge.neutral {
  color: var(--hermes-text-primary, #F4F4F5);
}

/* Tamaños */
.money-badge.sm { font-size: 0.85rem; }
.money-badge.md { font-size: 1rem; }
.money-badge.lg { font-size: 1.35rem; }
.money-badge.xl { font-size: 1.85rem; font-weight: 800; }
</style>

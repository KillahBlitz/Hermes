<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    percentage?: number | null
    invertSentiment?: boolean // True para gastos (subir es malo, bajar es bueno)
    label?: string
  }>(),
  {
    percentage: null,
    invertSentiment: false,
    label: 'vs mes anterior'
  }
)

const hasData = computed(() => props.percentage !== null && props.percentage !== undefined)

const isPositive = computed(() => (props.percentage ?? 0) > 0)
const isNegative = computed(() => (props.percentage ?? 0) < 0)

const isGood = computed(() => {
  if (!hasData.value) return false
  return props.invertSentiment ? isNegative.value : isPositive.value
})

const isBad = computed(() => {
  if (!hasData.value) return false
  return props.invertSentiment ? isPositive.value : isNegative.value
})

const formattedPercentage = computed(() => {
  if (!hasData.value) return 'Primer mes'
  const val = Math.abs(props.percentage!)
  const prefix = isPositive.value ? '+' : isNegative.value ? '-' : ''
  return `${prefix}${val.toFixed(1)}%`
})
</script>

<template>
  <div class="percentage-indicator" :class="{ 'is-good': isGood, 'is-bad': isBad, 'is-neutral': !hasData }">
    <span class="indicator-arrow" v-if="hasData">
      {{ isPositive ? '▲' : isNegative ? '▼' : '•' }}
    </span>
    <span class="indicator-value">{{ formattedPercentage }}</span>
    <span class="indicator-label" v-if="label">{{ label }}</span>
  </div>
</template>

<style scoped>
.percentage-indicator {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted, #94949E);
  transition: all 0.2s ease;
}

.percentage-indicator.is-good {
  color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.08);
  border-color: rgba(0, 255, 198, 0.25);
  box-shadow: 0 0 10px rgba(0, 255, 198, 0.12);
}

.percentage-indicator.is-bad {
  color: var(--hermes-accent-pink, #FF007F);
  background: rgba(255, 0, 127, 0.08);
  border-color: rgba(255, 0, 127, 0.25);
  box-shadow: 0 0 10px rgba(255, 0, 127, 0.12);
}

.indicator-arrow {
  font-size: 0.7rem;
}

.indicator-label {
  font-size: 0.72rem;
  opacity: 0.8;
  margin-left: 2px;
}
</style>

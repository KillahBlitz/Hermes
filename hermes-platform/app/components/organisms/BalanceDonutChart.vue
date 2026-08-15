<script setup lang="ts">
import { computed, ref } from 'vue'
import type { TotalsInfo } from '~/composables/useFinance'
import MoneyBadge from '~/components/atoms/MoneyBadge.vue'

const props = defineProps<{
  totals?: TotalsInfo | null
  loading?: boolean
}>()

const hoveredSlice = ref<'EXPENSE' | 'SAVINGS' | null>(null)

const income = computed(() => props.totals?.total_income || 0)
const expenses = computed(() => props.totals?.total_expenses || 0)
const netSavings = computed(() => props.totals?.net_savings ?? (income.value - expenses.value))
const isDeficit = computed(() => netSavings.value < 0)

// Porcentaje de gasto respecto al total de ingresos (o base 100%)
const expensePercentage = computed(() => {
  if (income.value <= 0) return expenses.value > 0 ? 100 : 0
  const pct = (expenses.value / income.value) * 100
  return Math.min(100, Math.max(0, pct))
})

const savingsPercentage = computed(() => {
  if (income.value <= 0) return 0
  const pct = 100 - expensePercentage.value
  return Math.max(0, pct)
})

// Configuración SVG Donut
const radius = 72
const strokeWidth = 24
const circumference = 2 * Math.PI * radius // ≈ 452.39

// Slices calculation
const expenseStrokeDash = computed(() => {
  if (income.value === 0 && expenses.value === 0) return `0 ${circumference}`
  if (isDeficit.value) return `${circumference} ${circumference}` // 100% gasto si hay déficit
  const len = (expensePercentage.value / 100) * circumference
  return `${len} ${circumference}`
})

const savingsStrokeDash = computed(() => {
  if (income.value === 0 && expenses.value === 0) return `0 ${circumference}`
  if (isDeficit.value) return `0 ${circumference}`
  const len = (savingsPercentage.value / 100) * circumference
  return `${len} ${circumference}`
})

const savingsStrokeOffset = computed(() => {
  if (isDeficit.value) return 0
  const expenseLen = (expensePercentage.value / 100) * circumference
  return -expenseLen
})
</script>

<template>
  <div class="balance-donut-card glass-panel" :class="{ 'is-deficit': isDeficit }">
    <div class="card-header">
      <div class="title-group">
        <h3 class="card-title">Balance de Ejecución</h3>
        <span class="card-subtitle">Resta de Gastos vs. Saldo a Favor</span>
      </div>

      <div class="header-badge" :class="isDeficit ? 'deficit' : 'surplus'">
        {{ isDeficit ? '⚠️ Déficit' : '✨ Superávit' }}
      </div>
    </div>

    <div class="card-body">
      <div v-if="loading" class="loading-overlay">
        <div class="spinner-border text-info" role="status"></div>
      </div>

      <div v-else-if="income === 0 && expenses === 0" class="empty-state">
        <span class="empty-icon">⚖️</span>
        <p>No hay ingresos ni gastos registrados en este periodo.</p>
      </div>

      <div v-else class="donut-display-row">
        <!-- SVG Donut -->
        <div class="svg-container">
          <svg class="donut-svg" viewBox="0 0 200 200">
            <!-- Círculo Base Background -->
            <circle
              cx="100"
              cy="100"
              :r="radius"
              fill="transparent"
              stroke="rgba(255, 255, 255, 0.04)"
              :stroke-width="strokeWidth"
            />

            <!-- Segmento Gastos (Rosa Neón) -->
            <circle
              class="donut-segment expense-segment"
              :class="{ highlighted: hoveredSlice === 'EXPENSE' }"
              cx="100"
              cy="100"
              :r="radius"
              fill="transparent"
              stroke="#FF007F"
              :stroke-width="hoveredSlice === 'EXPENSE' ? strokeWidth + 4 : strokeWidth"
              :stroke-dasharray="expenseStrokeDash"
              stroke-dashoffset="0"
              @mouseenter="hoveredSlice = 'EXPENSE'"
              @mouseleave="hoveredSlice = null"
            />

            <!-- Segmento Saldo a Favor / Ahorro (Verde Neón) -->
            <circle
              v-if="!isDeficit && savingsPercentage > 0"
              class="donut-segment savings-segment"
              :class="{ highlighted: hoveredSlice === 'SAVINGS' }"
              cx="100"
              cy="100"
              :r="radius"
              fill="transparent"
              stroke="#00FFC6"
              :stroke-width="hoveredSlice === 'SAVINGS' ? strokeWidth + 4 : strokeWidth"
              :stroke-dasharray="savingsStrokeDash"
              :stroke-dashoffset="savingsStrokeOffset"
              @mouseenter="hoveredSlice = 'SAVINGS'"
              @mouseleave="hoveredSlice = null"
            />
          </svg>

          <!-- Centro del Donut (Ingreso - Gasto) -->
          <div class="donut-center">
            <span class="center-tag">
              {{ isDeficit ? 'DÉFICIT' : 'SALDO A FAVOR' }}
            </span>
            <MoneyBadge
              :amount="netSavings"
              :type="isDeficit ? 'EXPENSE' : 'INCOME'"
              size="lg"
              :show-sign="false"
            />
            <span class="center-desc">
              {{ isDeficit ? 'Gastos superan ingresos' : `${expensePercentage.toFixed(0)}% gastado` }}
            </span>
          </div>
        </div>

        <!-- Leyenda Desglosada con Montos -->
        <div class="legend-column">
          <!-- Ingresos -->
          <div class="metric-row income-row">
            <div class="metric-left">
              <span class="dot income-dot"></span>
              <span class="metric-label">Ingresos Totales</span>
            </div>
            <MoneyBadge :amount="income" type="INCOME" size="md" :show-sign="true" />
          </div>

          <!-- Gastos Restados -->
          <div
            class="metric-row expense-row"
            :class="{ active: hoveredSlice === 'EXPENSE' }"
            @mouseenter="hoveredSlice = 'EXPENSE'"
            @mouseleave="hoveredSlice = null"
          >
            <div class="metric-left">
              <span class="dot expense-dot"></span>
              <span class="metric-label">Gastos Restados</span>
            </div>
            <div class="metric-right">
              <MoneyBadge :amount="expenses" type="EXPENSE" size="md" :show-sign="true" />
              <span class="pct-pill pink">{{ expensePercentage.toFixed(1) }}%</span>
            </div>
          </div>

          <div class="divider"></div>

          <!-- Saldo Restante / Neto -->
          <div
            class="metric-row net-row"
            :class="{ active: hoveredSlice === 'SAVINGS' }"
            @mouseenter="hoveredSlice = 'SAVINGS'"
            @mouseleave="hoveredSlice = null"
          >
            <div class="metric-left">
              <span class="dot net-dot" :class="isDeficit ? 'expense-dot' : 'income-dot'"></span>
              <span class="metric-label font-bold">Saldo Restante</span>
            </div>
            <div class="metric-right">
              <MoneyBadge :amount="netSavings" :type="isDeficit ? 'EXPENSE' : 'INCOME'" size="md" :show-sign="true" />
              <span v-if="!isDeficit" class="pct-pill teal">{{ savingsPercentage.toFixed(1) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.balance-donut-card {
  padding: 22px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
  flex-wrap: wrap;
  gap: 10px;
}

.card-title {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
}

.card-subtitle {
  font-size: 0.78rem;
  color: var(--hermes-text-muted, #94949E);
}

.header-badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 8px;
  border: 1px solid;
}

.header-badge.surplus {
  background: rgba(0, 255, 198, 0.1);
  color: var(--hermes-accent-teal, #00FFC6);
  border-color: rgba(0, 255, 198, 0.3);
  box-shadow: 0 0 10px rgba(0, 255, 198, 0.15);
}

.header-badge.deficit {
  background: rgba(255, 0, 127, 0.1);
  color: var(--hermes-accent-pink, #FF007F);
  border-color: rgba(255, 0, 127, 0.3);
  box-shadow: 0 0 10px rgba(255, 0, 127, 0.15);
}

.card-body {
  position: relative;
  flex: 1;
  min-height: 240px;
  display: flex;
  flex-direction: column;
}

.loading-overlay,
.empty-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.85rem;
  text-align: center;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}

.donut-display-row {
  display: flex;
  align-items: center;
  gap: 24px;
  height: 100%;
}

.svg-container {
  position: relative;
  width: 180px;
  height: 180px;
  flex-shrink: 0;
}

.donut-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.donut-segment {
  cursor: pointer;
  transition: stroke-width 0.2s ease, filter 0.2s ease;
}

.donut-segment.highlighted {
  filter: brightness(1.25) drop-shadow(0 0 8px currentColor);
}

.donut-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  pointer-events: none;
}

.center-tag {
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: var(--hermes-text-muted, #94949E);
}

.center-desc {
  font-size: 0.72rem;
  color: var(--hermes-text-muted, #94949E);
  font-weight: 600;
  margin-top: 2px;
}

.legend-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
}

.metric-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  transition: all 0.15s ease;
}

.metric-row:hover,
.metric-row.active {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.1);
}

.metric-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
}

.income-dot {
  background: var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 0 8px rgba(0, 255, 198, 0.4);
}

.expense-dot {
  background: var(--hermes-accent-pink, #FF007F);
  box-shadow: 0 0 8px rgba(255, 0, 127, 0.4);
}

.metric-label {
  font-size: 0.82rem;
  color: var(--hermes-text-primary, #F4F4F5);
}

.font-bold {
  font-weight: 700;
}

.metric-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pct-pill {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
}

.pct-pill.teal {
  background: rgba(0, 255, 198, 0.15);
  color: var(--hermes-accent-teal, #00FFC6);
}

.pct-pill.pink {
  background: rgba(255, 0, 127, 0.15);
  color: var(--hermes-accent-pink, #FF007F);
}

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.06);
}

@media (max-width: 768px) {
  .donut-display-row {
    flex-direction: column;
  }
}
</style>

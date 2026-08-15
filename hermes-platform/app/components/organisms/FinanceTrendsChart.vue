<script setup lang="ts">
import { computed, ref } from 'vue'
import type { MonthlyTrends, MonthTrendItem } from '~/composables/useFinance'
import MoneyBadge from '~/components/atoms/MoneyBadge.vue'

const props = defineProps<{
  trends?: MonthlyTrends | null
  loading?: boolean
}>()

const hoveredMonth = ref<MonthTrendItem | null>(null)

const months = computed(() => props.trends?.months || [])

const maxAmount = computed(() => {
  if (months.value.length === 0) return 1000
  let max = 0
  for (const m of months.value) {
    if (m.income > max) max = m.income
    if (m.expenses > max) max = m.expenses
  }
  return max > 0 ? max * 1.15 : 1000 // 15% de holgura superior
})

const formatAxisNumber = (val: number) => {
  if (val >= 1000000) return `$${(val / 1000000).toFixed(1)}M`
  if (val >= 1000) return `$${(val / 1000).toFixed(0)}k`
  return `$${val.toFixed(0)}`
}
</script>

<template>
  <div class="trends-chart-card glass-panel">
    <div class="chart-header">
      <div class="chart-title-group">
        <h3 class="chart-title">Tendencia Semestral</h3>
        <span class="chart-subtitle">Comparativa de Ingresos vs. Gastos</span>
      </div>

      <!-- Leyenda -->
      <div class="chart-legend">
        <div class="legend-item">
          <span class="legend-dot income"></span>
          <span class="legend-text">Ingresos</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot expense"></span>
          <span class="legend-text">Gastos</span>
        </div>
      </div>
    </div>

    <!-- Contenedor de la gráfica -->
    <div class="chart-container">
      <div v-if="loading" class="chart-loading-overlay">
        <div class="spinner-border text-info" role="status"></div>
      </div>

      <div v-else-if="months.length === 0" class="chart-empty-state">
        <span>📊</span>
        <p>No hay datos suficientes para mostrar el histórico.</p>
      </div>

      <div v-else class="chart-bars-wrapper">
        <!-- Eje Y con líneas guía -->
        <div class="grid-lines">
          <div class="grid-line" style="top: 0%;">
            <span class="grid-label">{{ formatAxisNumber(maxAmount) }}</span>
          </div>
          <div class="grid-line" style="top: 50%;">
            <span class="grid-label">{{ formatAxisNumber(maxAmount / 2) }}</span>
          </div>
          <div class="grid-line" style="top: 100%;">
            <span class="grid-label">$0</span>
          </div>
        </div>

        <!-- Barras de cada mes -->
        <div class="bars-columns">
          <div
            v-for="m in months"
            :key="`${m.year}-${m.month}`"
            class="month-bar-group"
            @mouseenter="hoveredMonth = m"
            @mouseleave="hoveredMonth = null"
          >
            <div class="bars-pair">
              <!-- Barra Ingreso -->
              <div class="bar-slot">
                <div
                  class="bar-fill income"
                  :style="{ height: `${Math.min(100, (m.income / maxAmount) * 100)}%` }"
                >
                  <div class="bar-glow"></div>
                </div>
              </div>

              <!-- Barra Gasto -->
              <div class="bar-slot">
                <div
                  class="bar-fill expense"
                  :style="{ height: `${Math.min(100, (m.expenses / maxAmount) * 100)}%` }"
                >
                  <div class="bar-glow"></div>
                </div>
              </div>
            </div>

            <!-- Etiqueta del Mes -->
            <span class="month-label">{{ m.label }}</span>
          </div>
        </div>
      </div>

      <!-- Tooltip Flotante de Detalle -->
      <div v-if="hoveredMonth" class="chart-tooltip glass-panel">
        <span class="tooltip-month">{{ hoveredMonth.label }}</span>
        <div class="tooltip-row">
          <span class="tooltip-dot income"></span>
          <span class="tooltip-label">Ingresos:</span>
          <MoneyBadge :amount="hoveredMonth.income" type="INCOME" size="sm" />
        </div>
        <div class="tooltip-row">
          <span class="tooltip-dot expense"></span>
          <span class="tooltip-label">Gastos:</span>
          <MoneyBadge :amount="hoveredMonth.expenses" type="EXPENSE" size="sm" />
        </div>
        <div class="tooltip-row net">
          <span class="tooltip-label">Balance:</span>
          <MoneyBadge :amount="hoveredMonth.savings" :type="hoveredMonth.savings >= 0 ? 'INCOME' : 'EXPENSE'" size="sm" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trends-chart-card {
  padding: 22px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.chart-title {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
}

.chart-subtitle {
  font-size: 0.78rem;
  color: var(--hermes-text-muted, #94949E);
}

.chart-legend {
  display: flex;
  align-items: center;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: var(--hermes-text-muted, #94949E);
  font-weight: 600;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
}

.legend-dot.income {
  background: var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 0 8px var(--hermes-accent-teal, #00FFC6);
}

.legend-dot.expense {
  background: var(--hermes-accent-pink, #FF007F);
  box-shadow: 0 0 8px var(--hermes-accent-pink, #FF007F);
}

.chart-container {
  position: relative;
  flex: 1;
  min-height: 240px;
  display: flex;
  flex-direction: column;
}

.chart-loading-overlay,
.chart-empty-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.85rem;
}

.chart-bars-wrapper {
  position: relative;
  flex: 1;
  padding: 10px 0 26px 45px;
  display: flex;
}

.grid-lines {
  position: absolute;
  top: 10px;
  bottom: 26px;
  left: 0;
  right: 0;
  pointer-events: none;
}

.grid-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(255, 255, 255, 0.05);
}

.grid-label {
  position: absolute;
  left: 0;
  top: -9px;
  font-size: 0.68rem;
  color: var(--hermes-text-muted, #94949E);
  font-family: 'JetBrains Mono', monospace;
}

.bars-columns {
  display: flex;
  justify-content: space-around;
  width: 100%;
  height: 100%;
  z-index: 2;
}

.month-bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 14%;
  height: 100%;
  cursor: pointer;
  position: relative;
  transition: transform 0.15s ease;
}

.month-bar-group:hover {
  transform: translateY(-2px);
}

.bars-pair {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  width: 100%;
  height: 100%;
  justify-content: center;
}

.bar-slot {
  width: 12px;
  height: 100%;
  display: flex;
  align-items: flex-end;
}

.bar-fill {
  width: 100%;
  border-radius: 4px 4px 0 0;
  min-height: 4px;
  position: relative;
  transition: height 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.bar-fill.income {
  background: linear-gradient(180deg, var(--hermes-accent-teal, #00FFC6) 0%, rgba(0, 255, 198, 0.3) 100%);
  box-shadow: 0 0 10px rgba(0, 255, 198, 0.3);
}

.bar-fill.expense {
  background: linear-gradient(180deg, var(--hermes-accent-pink, #FF007F) 0%, rgba(255, 0, 127, 0.3) 100%);
  box-shadow: 0 0 10px rgba(255, 0, 127, 0.3);
}

.month-label {
  position: absolute;
  bottom: -22px;
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--hermes-text-muted, #94949E);
  text-transform: capitalize;
}

.month-bar-group:hover .month-label {
  color: var(--hermes-text-primary, #F4F4F5);
}

/* Tooltip */
.chart-tooltip {
  position: absolute;
  bottom: 30px;
  right: 15px;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 6px;
  pointer-events: none;
  animation: fadeIn 0.15s ease-out;
}

.tooltip-month {
  font-weight: 800;
  font-size: 0.85rem;
  color: var(--hermes-text-primary, #F4F4F5);
  margin-bottom: 2px;
}

.tooltip-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.78rem;
  color: var(--hermes-text-muted, #94949E);
}

.tooltip-row.net {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-top: 4px;
  margin-top: 2px;
}

.tooltip-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.tooltip-dot.income { background: var(--hermes-accent-teal, #00FFC6); }
.tooltip-dot.expense { background: var(--hermes-accent-pink, #FF007F); }

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>

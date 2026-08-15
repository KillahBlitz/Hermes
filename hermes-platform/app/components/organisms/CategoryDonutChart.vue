<script setup lang="ts">
import { computed, ref } from 'vue'
import type { CategoryBreakdown, CategoryBreakdownItem } from '~/composables/useFinance'
import MoneyBadge from '~/components/atoms/MoneyBadge.vue'

const props = withDefaults(
  defineProps<{
    breakdown?: CategoryBreakdown | null
    breakdownType?: 'EXPENSE' | 'INCOME'
    title?: string
    subtitle?: string
    showToggle?: boolean
    loading?: boolean
  }>(),
  {
    breakdownType: 'EXPENSE',
    title: 'Distribución',
    subtitle: 'Por Categoría',
    showToggle: false,
    loading: false
  }
)

const emit = defineEmits<{
  (e: 'changeType', type: 'EXPENSE' | 'INCOME'): void
}>()

const hoveredCategory = ref<CategoryBreakdownItem | null>(null)

const items = computed(() => props.breakdown?.breakdown || [])
const totalAmount = computed(() => props.breakdown?.total || 0)

// Configuración de SVG Donut
const radius = 70
const strokeWidth = 22
const circumference = 2 * Math.PI * radius // ≈ 439.82

const slices = computed(() => {
  let accumulatedPercent = 0
  return items.value.map((item) => {
    const strokeDasharray = `${(item.percentage / 100) * circumference} ${circumference}`
    const strokeDashoffset = -((accumulatedPercent / 100) * circumference)
    accumulatedPercent += item.percentage
    return {
      ...item,
      strokeDasharray,
      strokeDashoffset
    }
  })
})
</script>

<template>
  <div class="donut-chart-card glass-panel" :class="breakdownType.toLowerCase()">
    <div class="donut-header">
      <div class="donut-title-group">
        <h3 class="donut-title">{{ title }}</h3>
        <span class="donut-subtitle">{{ subtitle }}</span>
      </div>

      <!-- Selector Gastos / Ingresos si está habilitado -->
      <div v-if="showToggle" class="type-toggle-pill">
        <button
          class="toggle-btn"
          :class="{ active: breakdownType === 'EXPENSE' }"
          @click="emit('changeType', 'EXPENSE')"
        >
          Gastos
        </button>
        <button
          class="toggle-btn"
          :class="{ active: breakdownType === 'INCOME' }"
          @click="emit('changeType', 'INCOME')"
        >
          Ingresos
        </button>
      </div>

      <div v-else class="type-badge-pill" :class="breakdownType.toLowerCase()">
        {{ breakdownType === 'EXPENSE' ? '💸 Gastos' : '💵 Ingresos' }}
      </div>
    </div>

    <div class="donut-body">
      <div v-if="loading" class="donut-loading-overlay">
        <div class="spinner-border text-info" role="status"></div>
      </div>

      <div v-else-if="items.length === 0" class="donut-empty-state">
        <span class="empty-icon">{{ breakdownType === 'EXPENSE' ? '💸' : '💵' }}</span>
        <p>No hay {{ breakdownType === 'EXPENSE' ? 'gastos' : 'ingresos' }} registrados este mes.</p>
      </div>

      <div v-else class="donut-content-grid">
        <!-- SVG Donut Chart -->
        <div class="svg-container">
          <svg class="donut-svg" viewBox="0 0 200 200">
            <!-- Círculo de Fondo -->
            <circle
              cx="100"
              cy="100"
              :r="radius"
              fill="transparent"
              stroke="rgba(255, 255, 255, 0.05)"
              :stroke-width="strokeWidth"
            />

            <!-- Segmentos del Donut -->
            <circle
              v-for="slice in slices"
              :key="slice.category_id"
              class="donut-segment"
              :class="{ highlighted: hoveredCategory?.category_id === slice.category_id }"
              cx="100"
              cy="100"
              :r="radius"
              fill="transparent"
              :stroke="slice.color || '#00FFC6'"
              :stroke-width="hoveredCategory?.category_id === slice.category_id ? strokeWidth + 4 : strokeWidth"
              :stroke-dasharray="slice.strokeDasharray"
              :stroke-dashoffset="slice.strokeDashoffset"
              @mouseenter="hoveredCategory = slice"
              @mouseleave="hoveredCategory = null"
            />
          </svg>

          <!-- Centro del Donut -->
          <div class="donut-center-info">
            <template v-if="hoveredCategory">
              <span class="center-icon">{{ hoveredCategory.icon }}</span>
              <span class="center-pct">{{ hoveredCategory.percentage }}%</span>
              <span class="center-label">{{ hoveredCategory.name }}</span>
            </template>
            <template v-else>
              <span class="center-title">TOTAL</span>
              <MoneyBadge :amount="totalAmount" :type="breakdownType" size="md" :show-sign="false" />
            </template>
          </div>
        </div>

        <!-- Lista de Categorías con Barra de Progreso -->
        <div class="donut-legend-list">
          <div
            v-for="item in items.slice(0, 5)"
            :key="item.category_id"
            class="legend-row"
            :class="{ active: hoveredCategory?.category_id === item.category_id }"
            @mouseenter="hoveredCategory = item"
            @mouseleave="hoveredCategory = null"
          >
            <div class="legend-row-top">
              <div class="legend-info">
                <span class="cat-icon">{{ item.icon }}</span>
                <span class="cat-name">{{ item.name }}</span>
              </div>
              <div class="legend-values">
                <MoneyBadge :amount="item.total" :type="breakdownType" size="sm" :show-sign="false" />
                <span class="cat-pct">({{ item.percentage }}%)</span>
              </div>
            </div>

            <div class="progress-track">
              <div
                class="progress-fill"
                :style="{
                  width: `${item.percentage}%`,
                  backgroundColor: item.color,
                  boxShadow: `0 0 8px ${item.color}50`
                }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.donut-chart-card {
  padding: 22px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.donut-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
  flex-wrap: wrap;
  gap: 10px;
}

.donut-title {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
}

.donut-subtitle {
  font-size: 0.78rem;
  color: var(--hermes-text-muted, #94949E);
}

.type-toggle-pill {
  display: flex;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 3px;
  border-radius: 10px;
}

.toggle-btn {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 7px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-btn.active {
  background: var(--hermes-bg-surface, #17171c);
  color: var(--hermes-text-primary, #F4F4F5);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

.type-badge-pill {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 8px;
  border: 1px solid;
}

.type-badge-pill.expense {
  background: rgba(255, 0, 127, 0.1);
  color: var(--hermes-accent-pink, #FF007F);
  border-color: rgba(255, 0, 127, 0.25);
}

.type-badge-pill.income {
  background: rgba(0, 255, 198, 0.1);
  color: var(--hermes-accent-teal, #00FFC6);
  border-color: rgba(0, 255, 198, 0.25);
}

.donut-body {
  position: relative;
  flex: 1;
  min-height: 240px;
  display: flex;
  flex-direction: column;
}

.donut-loading-overlay,
.donut-empty-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.85rem;
  text-align: center;
  padding: 20px;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}

.donut-content-grid {
  display: flex;
  align-items: center;
  gap: 20px;
  height: 100%;
}

.svg-container {
  position: relative;
  width: 170px;
  height: 170px;
  flex-shrink: 0;
}

.donut-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.donut-segment {
  cursor: pointer;
  transition: stroke-width 0.2s ease, opacity 0.2s ease;
}

.donut-segment.highlighted {
  filter: brightness(1.25);
}

.donut-center-info {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  pointer-events: none;
}

.center-title {
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: var(--hermes-text-muted, #94949E);
}

.center-icon {
  font-size: 1.1rem;
}

.center-pct {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  font-family: 'JetBrains Mono', monospace;
}

.center-label {
  font-size: 0.68rem;
  color: var(--hermes-text-muted, #94949E);
  max-width: 90px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.donut-legend-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 0;
}

.legend-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 4px 6px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.legend-row:hover,
.legend-row.active {
  background: rgba(255, 255, 255, 0.04);
}

.legend-row-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.legend-info {
  display: flex;
  align-items: center;
  gap: 6px;
  overflow: hidden;
}

.cat-icon { font-size: 0.9rem; }

.cat-name {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--hermes-text-primary, #F4F4F5);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.legend-values {
  display: flex;
  align-items: center;
  gap: 6px;
}

.cat-pct {
  font-size: 0.72rem;
  color: var(--hermes-text-muted, #94949E);
  font-family: 'JetBrains Mono', monospace;
}

.progress-track {
  height: 4px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.06);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.4s ease;
}

@media (max-width: 768px) {
  .donut-content-grid {
    flex-direction: column;
  }
}
</style>

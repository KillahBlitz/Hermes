<script setup lang="ts">
import type { TopInsights } from '~/composables/useFinance'
import MoneyBadge from '~/components/atoms/MoneyBadge.vue'

defineProps<{
  insights?: TopInsights | null
  monthName?: string
}>()
</script>

<template>
  <div v-if="insights?.highest_single_expense || insights?.highest_expense_category" class="insight-banner glass-panel">
    <div class="banner-badge">
      <span class="pulse-dot"></span>
      <span class="badge-text">INSIGHTS DE {{ monthName?.toUpperCase() || 'ESTE MES' }}</span>
    </div>

    <div class="insights-grid">
      <!-- Mayor gasto individual -->
      <div v-if="insights.highest_single_expense" class="insight-item">
        <div class="insight-icon-box pink">
          💸
        </div>
        <div class="insight-details">
          <span class="insight-label">Mayor Gasto Individual</span>
          <div class="insight-title-row">
            <span class="insight-main-title">{{ insights.highest_single_expense.title }}</span>
            <MoneyBadge :amount="insights.highest_single_expense.amount" type="EXPENSE" size="md" />
          </div>
          <span class="insight-meta">
            Categoría: <strong>{{ insights.highest_single_expense.category_name }}</strong>
          </span>
        </div>
      </div>

      <div v-if="insights.highest_single_expense && insights.highest_expense_category" class="insight-divider"></div>

      <!-- Categoría de mayor egreso -->
      <div v-if="insights.highest_expense_category" class="insight-item">
        <div class="insight-icon-box blue" :style="{ color: insights.highest_expense_category.color, backgroundColor: `${insights.highest_expense_category.color}20` }">
          {{ insights.highest_expense_category.icon }}
        </div>
        <div class="insight-details">
          <span class="insight-label">Categoría Principal de Gastos</span>
          <div class="insight-title-row">
            <span class="insight-main-title">{{ insights.highest_expense_category.category_name }}</span>
            <span class="category-pct-badge" :style="{ color: insights.highest_expense_category.color, borderColor: `${insights.highest_expense_category.color}40` }">
              {{ insights.highest_expense_category.percentage_of_total_expenses }}% del total
            </span>
          </div>
          <span class="insight-meta">
            Acumulado: <MoneyBadge :amount="insights.highest_expense_category.total_amount" type="EXPENSE" size="sm" />
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.insight-banner {
  padding: 18px 22px;
  border-radius: 16px;
  border-left: 4px solid var(--hermes-accent-blue, #00E5FF);
  background: linear-gradient(135deg, rgba(0, 229, 255, 0.04) 0%, rgba(23, 23, 28, 0.8) 100%);
  position: relative;
  overflow: hidden;
  margin-bottom: 24px;
}

.banner-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 8px var(--hermes-accent-blue, #00E5FF);
  animation: pulseGlow 1.8s infinite;
}

.badge-text {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: var(--hermes-accent-blue, #00E5FF);
}

.insights-grid {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.insight-item {
  display: flex;
  align-items: center;
  gap: 14px;
  flex: 1;
  min-width: 260px;
}

.insight-divider {
  width: 1px;
  height: 48px;
  background: rgba(255, 255, 255, 0.08);
}

.insight-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  flex-shrink: 0;
}

.insight-icon-box.pink {
  background: rgba(255, 0, 127, 0.15);
  color: var(--hermes-accent-pink, #FF007F);
  box-shadow: 0 0 12px rgba(255, 0, 127, 0.15);
}

.insight-icon-box.blue {
  background: rgba(0, 229, 255, 0.15);
  color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 12px rgba(0, 229, 255, 0.15);
}

.insight-details {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
}

.insight-label {
  font-size: 0.75rem;
  color: var(--hermes-text-muted, #94949E);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.insight-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.insight-main-title {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--hermes-text-primary, #F4F4F5);
}

.category-pct-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 6px;
  border: 1px solid;
  background: rgba(0, 0, 0, 0.2);
}

.insight-meta {
  font-size: 0.8rem;
  color: var(--hermes-text-muted, #94949E);
}

.insight-meta strong {
  color: var(--hermes-text-primary, #F4F4F5);
}

@keyframes pulseGlow {
  0% { transform: scale(0.9); opacity: 0.8; }
  50% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 14px var(--hermes-accent-blue, #00E5FF); }
  100% { transform: scale(0.9); opacity: 0.8; }
}

@media (max-width: 768px) {
  .insight-divider { display: none; }
}
</style>

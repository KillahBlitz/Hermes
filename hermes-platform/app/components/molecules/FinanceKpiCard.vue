<script setup lang="ts">
import MoneyBadge from '~/components/atoms/MoneyBadge.vue'
import PercentageIndicator from '~/components/atoms/PercentageIndicator.vue'

defineProps<{
  title: string
  amount: number
  type?: 'INCOME' | 'EXPENSE' | 'NEUTRAL'
  icon: string
  momPercentage?: number | null
  invertSentiment?: boolean
  accentColor?: string
  subtitle?: string
}>()
</script>

<template>
  <div class="finance-kpi-card glass-panel" :class="type ? type.toLowerCase() : 'neutral'">
    <div class="kpi-header">
      <span class="kpi-title">{{ title }}</span>
      <span class="kpi-icon-pill" :style="accentColor ? { color: accentColor, backgroundColor: `${accentColor}18` } : {}">
        {{ icon }}
      </span>
    </div>

    <div class="kpi-body">
      <MoneyBadge :amount="amount" :type="type" size="xl" :show-sign="false" />
    </div>

    <div class="kpi-footer">
      <PercentageIndicator
        v-if="momPercentage !== undefined"
        :percentage="momPercentage"
        :invert-sentiment="invertSentiment"
      />
      <span v-else-if="subtitle" class="kpi-subtitle">{{ subtitle }}</span>
    </div>
  </div>
</template>

<style scoped>
.finance-kpi-card {
  padding: 22px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 145px;
  position: relative;
  overflow: hidden;
  transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.25s ease, border-color 0.25s ease;
}

.finance-kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
  transition: opacity 0.3s ease;
}

.finance-kpi-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.finance-kpi-card.income:hover {
  border-color: rgba(0, 255, 198, 0.4);
  box-shadow: 0 12px 30px rgba(0, 255, 198, 0.15);
}

.finance-kpi-card.expense:hover {
  border-color: rgba(255, 0, 127, 0.4);
  box-shadow: 0 12px 30px rgba(255, 0, 127, 0.15);
}

.finance-kpi-card.neutral:hover {
  border-color: rgba(0, 229, 255, 0.4);
  box-shadow: 0 12px 30px rgba(0, 229, 255, 0.15);
}

.kpi-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.kpi-title {
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--hermes-text-muted, #94949E);
}

.kpi-icon-pill {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  background: rgba(255, 255, 255, 0.05);
}

.kpi-body {
  margin-bottom: 14px;
}

.kpi-footer {
  display: flex;
  align-items: center;
}

.kpi-subtitle {
  font-size: 0.78rem;
  color: var(--hermes-text-muted, #94949E);
  font-weight: 500;
}
</style>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  percentage: number
  totalTopics: number
  completedTopics: number
  color?: string
}>(), {
  color: '#00FFC6'
})

const barColor = computed(() => {
  if (props.percentage === 100) return 'var(--hermes-accent-teal, #00FFC6)'
  if (props.percentage >= 50) return 'var(--hermes-accent-blue, #00E5FF)'
  return '#FFD166'
})
</script>

<template>
  <div class="progress-bar-container">
    <div class="progress-bar-header">
      <span class="progress-count">{{ completedTopics }}/{{ totalTopics }} temas</span>
      <span class="progress-pct" :style="{ color: barColor }">{{ Math.round(percentage) }}%</span>
    </div>
    <div class="progress-track">
      <div
        class="progress-fill"
        :style="{
          width: `${Math.min(Math.max(percentage, 0), 100)}%`,
          background: percentage === 100 
            ? 'linear-gradient(90deg, #00E5FF 0%, #00FFC6 100%)' 
            : 'linear-gradient(90deg, #FF007F 0%, #00E5FF 100%)'
        }"
      />
    </div>
  </div>
</template>

<style scoped>
.progress-bar-container {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.progress-bar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.78rem;
  font-weight: 600;
}

.progress-count {
  color: var(--hermes-text-muted);
}

.progress-pct {
  font-weight: 700;
  font-feature-settings: 'tnum';
}

.progress-track {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.4);
}
</style>

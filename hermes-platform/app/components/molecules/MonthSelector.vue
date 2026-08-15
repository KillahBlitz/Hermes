<script setup lang="ts">
import { computed, ref } from 'vue'

const props = defineProps<{
  year: number
  month: number
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'change', year: number, month: number): void
  (e: 'prev'): void
  (e: 'next'): void
}>()

const showPicker = ref(false)
const selectedPickerYear = ref(props.year)

const MONTH_NAMES = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

const currentMonthName = computed(() => {
  if (props.month >= 1 && props.month <= 12) {
    return MONTH_NAMES[props.month - 1]
  }
  return String(props.month)
})

const isCurrentActualMonth = computed(() => {
  const now = new Date()
  return props.year === now.getFullYear() && props.month === (now.getMonth() + 1)
})

const openPicker = () => {
  selectedPickerYear.value = props.year
  showPicker.value = !showPicker.value
}

const selectMonth = (mIndex: number) => {
  emit('change', selectedPickerYear.value, mIndex + 1)
  showPicker.value = false
}

const goToToday = () => {
  const now = new Date()
  emit('change', now.getFullYear(), now.getMonth() + 1)
  showPicker.value = false
}
</script>

<template>
  <div class="month-selector-wrapper">
    <div class="month-selector glass-panel">
      <button
        class="nav-btn"
        title="Mes anterior"
        :disabled="loading"
        @click="emit('prev')"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>

      <button class="current-period-btn" :disabled="loading" @click="openPicker">
        <span class="calendar-icon">📅</span>
        <span class="period-text">{{ currentMonthName }} {{ year }}</span>
        <span class="dropdown-arrow">▼</span>
      </button>

      <button
        class="nav-btn"
        title="Mes siguiente"
        :disabled="loading"
        @click="emit('next')"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>

      <button
        v-if="!isCurrentActualMonth"
        class="today-quick-btn"
        title="Ir al mes actual"
        @click="goToToday"
      >
        Mes Actual
      </button>
    </div>

    <!-- Dropdown Picker -->
    <div v-if="showPicker" class="picker-popover glass-panel">
      <div class="picker-header">
        <button class="year-nav-btn" @click="selectedPickerYear--">«</button>
        <span class="picker-year-label">{{ selectedPickerYear }}</span>
        <button class="year-nav-btn" @click="selectedPickerYear++">»</button>
      </div>

      <div class="months-grid">
        <button
          v-for="(mName, idx) in MONTH_NAMES"
          :key="idx"
          class="month-choice-btn"
          :class="{ active: year === selectedPickerYear && month === (idx + 1) }"
          @click="selectMonth(idx)"
        >
          {{ mName.slice(0, 3) }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.month-selector-wrapper {
  position: relative;
  display: inline-block;
}

.month-selector {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 14px;
}

.nav-btn {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted, #94949E);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary, #F4F4F5);
}

.nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.current-period-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary, #F4F4F5);
  padding: 6px 14px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.current-period-btn:hover:not(:disabled) {
  border-color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.05);
  box-shadow: 0 0 14px rgba(0, 255, 198, 0.12);
}

.calendar-icon {
  font-size: 1rem;
}

.dropdown-arrow {
  font-size: 0.6rem;
  color: var(--hermes-text-muted, #94949E);
  transition: transform 0.2s ease;
}

.today-quick-btn {
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.3);
  color: var(--hermes-accent-blue, #00E5FF);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.today-quick-btn:hover {
  background: rgba(0, 229, 255, 0.2);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
}

/* Popover Picker */
.picker-popover {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  z-index: 50;
  width: 260px;
  padding: 16px;
  border-radius: 16px;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  animation: fadeInDown 0.18s ease-out;
}

.picker-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.year-nav-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-primary, #F4F4F5);
  width: 28px;
  height: 28px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.picker-year-label {
  font-weight: 800;
  font-size: 1rem;
  color: var(--hermes-text-primary, #F4F4F5);
}

.months-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.month-choice-btn {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: var(--hermes-text-muted, #94949E);
  padding: 8px 4px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.month-choice-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary, #F4F4F5);
}

.month-choice-btn.active {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  font-weight: 800;
  box-shadow: 0 0 12px rgba(0, 255, 198, 0.4);
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

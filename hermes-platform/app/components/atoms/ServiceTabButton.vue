<script setup lang="ts">
defineProps<{
  active: boolean
  label: string
  count?: number
}>()

defineEmits<{
  (e: 'click'): void
}>()
</script>

<template>
  <button
    class="service-tab-btn"
    :class="{ active }"
    type="button"
    @click="$emit('click')"
  >
    <span class="tab-icon-wrapper">
      <slot name="icon" />
    </span>
    <span class="tab-label">{{ label }}</span>
    <span v-if="count !== undefined && count > 0" class="tab-badge">
      {{ count }}
    </span>
  </button>
</template>

<style scoped>
.service-tab-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  color: var(--hermes-text-muted);
  font-family: inherit;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
}

.service-tab-btn:hover {
  background: rgba(255, 255, 255, 0.07);
  color: var(--hermes-text-primary);
  border-color: rgba(255, 255, 255, 0.12);
  transform: translateY(-1px);
}

.service-tab-btn.active {
  background: linear-gradient(135deg, rgba(0, 229, 255, 0.15), rgba(255, 0, 127, 0.15));
  border-color: rgba(0, 229, 255, 0.4);
  color: #ffffff;
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.2), inset 0 0 12px rgba(255, 0, 127, 0.1);
}

.service-tab-btn.active::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20%;
  right: 20%;
  height: 2px;
  background: linear-gradient(90deg, var(--hermes-accent-blue), var(--hermes-accent-pink));
  border-radius: 2px;
}

.tab-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.25s ease;
}

.service-tab-btn:hover .tab-icon-wrapper {
  transform: scale(1.1);
}

.service-tab-btn.active .tab-icon-wrapper {
  color: var(--hermes-accent-blue);
}

.tab-badge {
  font-size: 0.72rem;
  padding: 2px 7px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted);
  font-weight: 700;
}

.service-tab-btn.active .tab-badge {
  background: var(--hermes-accent-pink);
  color: #ffffff;
}
</style>

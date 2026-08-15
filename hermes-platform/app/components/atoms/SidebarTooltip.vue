<script setup lang="ts">
defineProps<{
  text: string
  visible: boolean
}>()
</script>

<template>
  <Transition name="tooltip-fade">
    <div v-if="visible" class="sidebar-tooltip">
      <span class="tooltip-text">{{ text }}</span>
    </div>
  </Transition>
</template>

<style scoped>
.sidebar-tooltip {
  position: absolute;
  left: calc(100% + 12px);
  top: 50%;
  transform: translateY(-50%);
  z-index: 200;
  pointer-events: none;
  white-space: nowrap;
}

.tooltip-text {
  display: inline-block;
  padding: 6px 14px;
  background: rgba(23, 23, 28, 0.88);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: var(--hermes-text-primary);
  font-size: 0.8rem;
  font-weight: 500;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5),
              0 0 8px rgba(0, 229, 255, 0.12);
}

/* Transition */
.tooltip-fade-enter-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.tooltip-fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.tooltip-fade-enter-from {
  opacity: 0;
  transform: translateY(-50%) translateX(-6px);
}
.tooltip-fade-leave-to {
  opacity: 0;
  transform: translateY(-50%) translateX(-6px);
}
</style>

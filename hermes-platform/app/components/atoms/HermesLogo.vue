<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
    animated?: boolean
    glow?: boolean
  }>(),
  {
    size: 'md',
    animated: true,
    glow: true
  }
)

const sizeClass = computed(() => `logo-size-${props.size}`)
</script>

<template>
  <div
    class="hermes-logo-wrapper"
    :class="[
      sizeClass,
      { 'is-animated': animated, 'has-glow': glow }
    ]"
  >
    <div v-if="glow" class="logo-ambient-halo" />
    <img
      src="/logo.png"
      alt="Hermes Platform Logo"
      class="logo-image"
      loading="eager"
    >
  </div>
</template>

<style scoped>
.hermes-logo-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  flex-shrink: 0;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: inherit;
  position: relative;
  z-index: 2;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Ambient Halo */
.logo-ambient-halo {
  position: absolute;
  inset: -4px;
  border-radius: inherit;
  background: radial-gradient(
    circle,
    rgba(0, 229, 255, 0.4) 0%,
    rgba(255, 0, 127, 0.3) 60%,
    transparent 80%
  );
  filter: blur(8px);
  opacity: 0.7;
  z-index: 1;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

/* Sizes */
.logo-size-xs {
  width: 24px;
  height: 24px;
  border-radius: 6px;
}

.logo-size-sm {
  width: 34px;
  height: 34px;
  border-radius: 8px;
}

.logo-size-md {
  width: 48px;
  height: 48px;
  border-radius: 12px;
}

.logo-size-lg {
  width: 72px;
  height: 72px;
  border-radius: 16px;
}

.logo-size-xl {
  width: 96px;
  height: 96px;
  border-radius: 20px;
}

/* Animations */
.hermes-logo-wrapper.is-animated .logo-ambient-halo {
  animation: logo-halo-breathe 4s ease-in-out infinite alternate;
}

.hermes-logo-wrapper.is-animated .logo-image {
  animation: logo-subtle-float 5s ease-in-out infinite alternate;
}

.hermes-logo-wrapper:hover .logo-image {
  transform: translateY(-2px) scale(1.04);
  border-color: rgba(0, 229, 255, 0.5);
  box-shadow: 0 8px 24px rgba(0, 229, 255, 0.35);
}

.hermes-logo-wrapper:hover .logo-ambient-halo {
  opacity: 1;
  filter: blur(12px);
}

@keyframes logo-halo-breathe {
  0% {
    transform: scale(0.95);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.12);
    opacity: 0.85;
  }
  100% {
    transform: scale(0.95);
    opacity: 0.5;
  }
}

@keyframes logo-subtle-float {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(-2px);
  }
}
</style>

<script setup lang="ts">
interface Props {
  variant?: 'blue' | 'pink' | 'teal' | 'outline' | 'ghost'
  loading?: boolean
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
  block?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'blue',
  loading: false,
  disabled: false,
  type: 'button',
  block: false,
})

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="[
      'hermes-btn',
      `hermes-btn-${variant}`,
      { 'hermes-btn-block': block, 'hermes-btn-loading': loading }
    ]"
    @click="emit('click', $event)"
  >
    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true" />
    <slot />
  </button>
</template>

<style scoped>
.hermes-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  font-weight: 600;
  font-size: 0.95rem;
  border-radius: 12px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  text-decoration: none;
  letter-spacing: -0.01em;
}

.hermes-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.hermes-btn-block {
  width: 100%;
}

/* Blue Variant */
.hermes-btn-blue {
  background: linear-gradient(135deg, #00E5FF 0%, #00B4D8 100%);
  color: #09090B;
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.35);
}

.hermes-btn-blue:hover:not(:disabled) {
  background: linear-gradient(135deg, #33EBFF 0%, #00C2E8 100%);
  box-shadow: 0 0 30px rgba(0, 229, 255, 0.6);
  transform: translateY(-2px);
}

/* Pink Variant */
.hermes-btn-pink {
  background: linear-gradient(135deg, #FF007F 0%, #E0006E 100%);
  color: #FFFFFF;
  box-shadow: 0 0 20px rgba(255, 0, 127, 0.35);
}

.hermes-btn-pink:hover:not(:disabled) {
  background: linear-gradient(135deg, #FF2E93 0%, #F50079 100%);
  box-shadow: 0 0 30px rgba(255, 0, 127, 0.6);
  transform: translateY(-2px);
}

/* Teal Variant */
.hermes-btn-teal {
  background: linear-gradient(135deg, #00FFC6 0%, #00D1A3 100%);
  color: #09090B;
  box-shadow: 0 0 20px rgba(0, 255, 198, 0.35);
}

.hermes-btn-teal:hover:not(:disabled) {
  box-shadow: 0 0 30px rgba(0, 255, 198, 0.6);
  transform: translateY(-2px);
}

/* Outline Variant */
.hermes-btn-outline {
  background: rgba(255, 255, 255, 0.03);
  border-color: rgba(255, 255, 255, 0.15);
  color: var(--hermes-text-primary);
}

.hermes-btn-outline:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  border-color: var(--hermes-accent-blue);
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.25);
  transform: translateY(-2px);
}

/* Ghost Variant */
.hermes-btn-ghost {
  background: transparent;
  color: var(--hermes-text-muted);
}

.hermes-btn-ghost:hover:not(:disabled) {
  color: var(--hermes-text-primary);
  background: rgba(255, 255, 255, 0.05);
}
</style>

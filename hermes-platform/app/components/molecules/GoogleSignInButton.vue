<script setup lang="ts">
interface Props {
  loading?: boolean
  disabled?: boolean
}

withDefaults(defineProps<Props>(), {
  loading: false,
  disabled: false
})

const emit = defineEmits<{
  (e: 'click'): void
}>()
</script>

<template>
  <button
    type="button"
    class="google-btn"
    :disabled="disabled || loading"
    @click="emit('click')"
  >
    <div class="google-icon-wrapper">
      <span v-if="loading" class="spinner-border spinner-border-sm text-light" role="status" aria-hidden="true" />
      <svg
        v-else
        class="google-icon"
        viewBox="0 0 24 24"
        width="22"
        height="22"
        xmlns="https://www.w3.org/2000/svg"
      >
        <path
          fill="#4285F4"
          d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.17z"
        />
        <path
          fill="#34A853"
          d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"
        />
        <path
          fill="#FBBC05"
          d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.99 0 12s.45 3.82 1.25 5.42l4.03-3.15z"
        />
        <path
          fill="#EA4335"
          d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"
        />
      </svg>
    </div>
    <span class="google-btn-text">
      {{ loading ? 'Conectando con Google...' : 'Continuar con Google' }}
    </span>
  </button>
</template>

<style scoped>
.google-btn {
  position: relative;
  width: 100%;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: rgba(39, 39, 42, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 14px;
  color: var(--hermes-text-primary);
  font-weight: 600;
  font-size: 0.98rem;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
}

.google-btn::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: 15px;
  padding: 1px;
  background: linear-gradient(135deg, var(--hermes-accent-blue), transparent 45%, var(--hermes-accent-pink));
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0.5;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.google-btn:hover:not(:disabled) {
  background: rgba(50, 50, 56, 0.95);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 229, 255, 0.25), 0 0 20px rgba(255, 0, 127, 0.2);
}

.google-btn:hover:not(:disabled)::before {
  opacity: 1;
}

.google-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.google-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.google-btn-text {
  letter-spacing: -0.01em;
}
</style>

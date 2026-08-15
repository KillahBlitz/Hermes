<script setup lang="ts">
const props = defineProps<{
  isPinned: boolean
  isExpanded: boolean
}>()

const emit = defineEmits<{
  toggle: []
}>()
</script>

<template>
  <button
    class="pin-toggle"
    :class="{ 'is-pinned': isPinned, 'is-visible': isExpanded }"
    :title="isPinned ? 'Desfijar menú' : 'Fijar menú'"
    @click.stop="emit('toggle')"
  >
    <svg
      class="pin-icon"
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <!-- Thumbtack / Pin icon -->
      <path d="M12 17v5" />
      <path d="M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24V16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V7a1 1 0 0 1 1-1 1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1 1 1 0 0 1 1 1z" />
    </svg>
  </button>
</template>

<style scoped>
.pin-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--hermes-text-muted);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  opacity: 0;
  pointer-events: none;
}

.pin-toggle.is-visible {
  opacity: 0.6;
  pointer-events: auto;
}

.pin-toggle.is-visible:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.06);
}

.pin-toggle.is-pinned {
  opacity: 1;
  color: var(--hermes-accent-blue);
  pointer-events: auto;
}

.pin-toggle.is-pinned:hover {
  background: rgba(0, 229, 255, 0.08);
}

.pin-icon {
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1),
              filter 0.3s ease;
}

.pin-toggle.is-pinned .pin-icon {
  transform: rotate(45deg);
  filter: drop-shadow(0 0 6px rgba(0, 229, 255, 0.6));
}
</style>

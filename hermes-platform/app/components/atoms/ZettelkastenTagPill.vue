<script setup lang="ts">
const props = withDefaults(defineProps<{
  tag: string
  active?: boolean
  clickable?: boolean
}>(), {
  active: false,
  clickable: true
})

const emit = defineEmits<{
  (e: 'click', tag: string): void
}>()
</script>

<template>
  <button
    type="button"
    class="tag-pill"
    :class="{ 'is-active': active, 'is-clickable': clickable }"
    @click="clickable ? emit('click', tag) : null"
  >
    <span class="tag-hash">#</span>
    <span class="tag-name">{{ tag }}</span>
  </button>
</template>

<style scoped>
.tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  color: var(--hermes-text-muted);
  font-size: 0.75rem;
  font-weight: 600;
  cursor: default;
  transition: all 0.2s ease;
  font-family: inherit;
}

.is-clickable {
  cursor: pointer;
}

.is-clickable:hover {
  background: rgba(0, 229, 255, 0.12);
  border-color: rgba(0, 229, 255, 0.4);
  color: var(--hermes-accent-blue, #00E5FF);
  transform: translateY(-1px);
}

.tag-pill.is-active {
  background: rgba(0, 229, 255, 0.2);
  border-color: var(--hermes-accent-blue, #00E5FF);
  color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.25);
}

.tag-hash {
  color: var(--hermes-accent-pink, #FF007F);
  font-weight: 800;
}
</style>

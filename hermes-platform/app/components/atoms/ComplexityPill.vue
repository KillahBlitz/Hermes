<script setup lang="ts">
withDefaults(
  defineProps<{
    complexity: 'XS' | 'S' | 'M' | 'L' | 'XL' | string
    size?: 'sm' | 'md'
  }>(),
  {
    size: 'md'
  }
)
</script>

<template>
  <span class="complexity-pill" :class="[complexity.toLowerCase(), size]" :title="`Complejidad ${complexity}`">
    <span class="pts-prefix">⚡</span>
    <span class="complexity-text">{{ complexity }}</span>
  </span>
</template>

<style scoped>
.complexity-pill {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  border-radius: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.04);
  color: var(--hermes-text-primary, #F4F4F5);
}

.complexity-pill.sm {
  padding: 1px 6px;
  font-size: 0.7rem;
}

.complexity-pill.md {
  padding: 2px 8px;
  font-size: 0.75rem;
}

.complexity-pill.xs { color: #06D6A0; border-color: rgba(6, 214, 160, 0.3); }
.complexity-pill.s  { color: #00E5FF; border-color: rgba(0, 229, 255, 0.3); }
.complexity-pill.m  { color: #FFD166; border-color: rgba(255, 209, 102, 0.3); }
.complexity-pill.l  { color: #FF007F; border-color: rgba(255, 0, 127, 0.3); }
.complexity-pill.xl { color: #F72585; border-color: rgba(247, 37, 133, 0.4); background: rgba(247, 37, 133, 0.1); }

.pts-prefix {
  font-size: 0.75em;
  opacity: 0.8;
}
</style>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    amount: number
    currency?: string
    size?: 'sm' | 'md' | 'lg'
  }>(),
  {
    currency: 'MXN',
    size: 'md'
  }
)

const formatted = computed(() => {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: props.currency || 'MXN',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(props.amount)
})
</script>

<template>
  <span class="wishlist-price-tag" :class="size">
    <span class="price-value">{{ formatted }}</span>
  </span>
</template>

<style scoped>
.wishlist-price-tag {
  display: inline-flex;
  align-items: center;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.1);
  border: 1px solid rgba(0, 255, 198, 0.3);
  border-radius: 8px;
  letter-spacing: -0.02em;
  box-shadow: 0 0 12px rgba(0, 255, 198, 0.12);
}

.wishlist-price-tag.sm {
  padding: 2px 7px;
  font-size: 0.75rem;
}

.wishlist-price-tag.md {
  padding: 3px 10px;
  font-size: 0.9rem;
}

.wishlist-price-tag.lg {
  padding: 4px 14px;
  font-size: 1.15rem;
}
</style>

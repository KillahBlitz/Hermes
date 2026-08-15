<script setup lang="ts">
import { computed } from 'vue'
import type { Transaction } from '~/composables/useFinance'
import CategoryTag from '~/components/atoms/CategoryTag.vue'
import MoneyBadge from '~/components/atoms/MoneyBadge.vue'

const props = defineProps<{
  transaction: Transaction
}>()

const emit = defineEmits<{
  (e: 'edit', tx: Transaction): void
  (e: 'delete', tx: Transaction): void
}>()

const formattedDate = computed(() => {
  if (!props.transaction.date) return ''
  const d = new Date(props.transaction.date)
  return new Intl.DateTimeFormat('es-MX', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  }).format(d)
})
</script>

<template>
  <div class="transaction-row glass-panel" :class="transaction.type.toLowerCase()">
    <!-- Izquierda: Fecha y Categoría -->
    <div class="tx-left">
      <span class="tx-date">{{ formattedDate }}</span>
      <CategoryTag
        :name="transaction.category?.name || 'General'"
        :icon="transaction.category?.icon || '🏷️'"
        :color="transaction.category?.color || '#00FFC6'"
        size="sm"
      />
    </div>

    <!-- Centro: Título y Notas -->
    <div class="tx-center">
      <span class="tx-title" :title="transaction.title">{{ transaction.title }}</span>
      <span v-if="transaction.notes" class="tx-notes" :title="transaction.notes">{{ transaction.notes }}</span>
    </div>

    <!-- Derecha: Monto y Acciones -->
    <div class="tx-right">
      <MoneyBadge
        :amount="transaction.amount"
        :type="transaction.type"
        size="lg"
        :show-sign="true"
      />

      <div class="tx-actions">
        <button class="action-btn edit-btn" title="Editar movimiento" @click="emit('edit', transaction)">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </button>
        <button class="action-btn delete-btn" title="Eliminar movimiento" @click="emit('delete', transaction)">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.transaction-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 18px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(23, 23, 28, 0.6);
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.transaction-row:hover {
  transform: translateX(4px);
  background: rgba(23, 23, 28, 0.95);
  border-color: rgba(255, 255, 255, 0.12);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.transaction-row.income:hover {
  border-left: 3px solid var(--hermes-accent-teal, #00FFC6);
}

.transaction-row.expense:hover {
  border-left: 3px solid var(--hermes-accent-pink, #FF007F);
}

.tx-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 140px;
}

.tx-date {
  font-size: 0.72rem;
  color: var(--hermes-text-muted, #94949E);
  font-weight: 500;
  font-family: 'JetBrains Mono', monospace;
}

.tx-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.tx-title {
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--hermes-text-primary, #F4F4F5);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tx-notes {
  font-size: 0.78rem;
  color: var(--hermes-text-muted, #94949E);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tx-right {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.tx-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.transaction-row:hover .tx-actions {
  opacity: 1;
}

.action-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted, #94949E);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.edit-btn:hover {
  background: rgba(0, 229, 255, 0.15);
  border-color: var(--hermes-accent-blue, #00E5FF);
  color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.25);
}

.delete-btn:hover {
  background: rgba(255, 0, 127, 0.15);
  border-color: var(--hermes-accent-pink, #FF007F);
  color: var(--hermes-accent-pink, #FF007F);
  box-shadow: 0 0 10px rgba(255, 0, 127, 0.25);
}

@media (max-width: 640px) {
  .transaction-row {
    flex-direction: column;
    align-items: flex-start;
  }
  .tx-right {
    width: 100%;
    justify-content: space-between;
  }
}
</style>

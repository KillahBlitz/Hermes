<script setup lang="ts">
import type { Category, Transaction } from '~/composables/useFinance'
import TransactionRow from '~/components/molecules/TransactionRow.vue'

defineProps<{
  transactions: Transaction[]
  categories: Category[]
  filterType: 'all' | 'INCOME' | 'EXPENSE'
  filterCategoryId: string
  searchQuery: string
  page: number
  totalPages: number
  totalTransactions: number
  hasNextPage: boolean
  hasPrevPage: boolean
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'changeFilterType', type: 'all' | 'INCOME' | 'EXPENSE'): void
  (e: 'changeFilterCategory', catId: string): void
  (e: 'search', q: string): void
  (e: 'nextPage'): void
  (e: 'prevPage'): void
  (e: 'newTransaction'): void
  (e: 'openCategoryManager'): void
  (e: 'editTransaction', tx: Transaction): void
  (e: 'deleteTransaction', tx: Transaction): void
}>()

const onSearchInput = (ev: Event) => {
  const target = ev.target as HTMLInputElement
  emit('search', target.value)
}
</script>

<template>
  <div class="transaction-list-section glass-panel">
    <!-- Header de la sección -->
    <div class="section-top-bar">
      <div class="title-group">
        <h3 class="section-title">Movimientos Registrados</h3>
        <span class="section-badge">{{ totalTransactions }} movimientos</span>
      </div>

      <div class="top-actions">
        <button class="secondary-btn" @click="emit('openCategoryManager')">
          <span>🏷️</span> Categorías
        </button>
        <button class="primary-btn glow-teal" @click="emit('newTransaction')">
          <span>+</span> Nuevo Movimiento
        </button>
      </div>
    </div>

    <!-- Barra de Filtros y Búsqueda -->
    <div class="filters-bar">
      <!-- Filtro Tipo -->
      <div class="type-filter-group">
        <button
          class="filter-pill"
          :class="{ active: filterType === 'all' }"
          @click="emit('changeFilterType', 'all')"
        >
          Todos
        </button>
        <button
          class="filter-pill income"
          :class="{ active: filterType === 'INCOME' }"
          @click="emit('changeFilterType', 'INCOME')"
        >
          🟢 Ingresos
        </button>
        <button
          class="filter-pill expense"
          :class="{ active: filterType === 'EXPENSE' }"
          @click="emit('changeFilterType', 'EXPENSE')"
        >
          🔴 Gastos
        </button>
      </div>

      <!-- Filtro Categoría -->
      <div class="select-wrapper">
        <select
          :value="filterCategoryId"
          class="category-select"
          @change="emit('changeFilterCategory', ($event.target as HTMLSelectElement).value)"
        >
          <option value="">Todas las categorías</option>
          <option
            v-for="cat in categories"
            :key="cat.id"
            :value="cat.id"
          >
            {{ cat.icon }} {{ cat.name }} ({{ cat.type === 'INCOME' ? 'Ingreso' : 'Gasto' }})
          </option>
        </select>
      </div>

      <!-- Buscador -->
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input
          :value="searchQuery"
          type="text"
          placeholder="Buscar por concepto o notas..."
          class="search-input"
          @input="onSearchInput"
        />
      </div>
    </div>

    <!-- Lista de Transacciones -->
    <div class="transactions-container">
      <!-- Loading Skeletons -->
      <div v-if="loading" class="skeletons-list">
        <div v-for="i in 3" :key="i" class="tx-skeleton shimmer"></div>
      </div>

      <!-- Estado Vacío -->
      <div v-else-if="transactions.length === 0" class="empty-state">
        <span class="empty-icon">💸</span>
        <h4 class="empty-title">Sin movimientos en este periodo</h4>
        <p class="empty-desc">No se encontraron ingresos ni gastos con los filtros seleccionados.</p>
        <button class="primary-btn glow-teal sm" @click="emit('newTransaction')">
          + Registrar primer movimiento
        </button>
      </div>

      <!-- Filas de Transacciones -->
      <div v-else class="transactions-rows">
        <TransactionRow
          v-for="tx in transactions"
          :key="tx.id"
          :transaction="tx"
          @edit="emit('editTransaction', tx)"
          @delete="emit('deleteTransaction', tx)"
        />
      </div>
    </div>

    <!-- Barra de Paginación -->
    <div v-if="totalTransactions > 0" class="pagination-bar">
      <span class="page-info">10 por página • Total {{ totalTransactions }}</span>

      <div class="page-controls">
        <button
          class="page-btn"
          :disabled="!hasPrevPage || loading"
          @click="emit('prevPage')"
        >
          ← Anterior
        </button>

        <span class="current-page-badge">
          Página {{ page }} de {{ totalPages }}
        </span>

        <button
          class="page-btn"
          :disabled="!hasNextPage || loading"
          @click="emit('nextPage')"
        >
          Siguiente →
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.transaction-list-section {
  padding: 24px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 14px;
}

.title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
}

.section-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--hermes-text-muted, #94949E);
}

.top-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.primary-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  font-weight: 700;
  font-size: 0.88rem;
  padding: 8px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn.sm {
  font-size: 0.8rem;
  padding: 6px 12px;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 16px rgba(0, 255, 198, 0.4);
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-primary, #F4F4F5);
  font-weight: 600;
  font-size: 0.88rem;
  padding: 8px 14px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

/* Filtros */
.filters-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.type-filter-group {
  display: flex;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  padding: 3px;
  border-radius: 10px;
}

.filter-pill {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.8rem;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.filter-pill.active {
  background: rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-primary, #F4F4F5);
}

.filter-pill.income.active {
  background: rgba(0, 255, 198, 0.15);
  color: var(--hermes-accent-teal, #00FFC6);
}

.filter-pill.expense.active {
  background: rgba(255, 0, 127, 0.15);
  color: var(--hermes-accent-pink, #FF007F);
}

.select-wrapper {
  position: relative;
}

.category-select {
  background: rgba(23, 23, 28, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary, #F4F4F5);
  padding: 7px 12px;
  border-radius: 10px;
  font-size: 0.82rem;
  font-weight: 500;
  outline: none;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.category-select:focus {
  border-color: var(--hermes-accent-teal, #00FFC6);
}

.category-select option {
  background: #17171c;
  color: #F4F4F5;
}

.search-box {
  flex: 1;
  min-width: 200px;
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 10px;
  font-size: 0.8rem;
  pointer-events: none;
  opacity: 0.6;
}

.search-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 7px 12px 7px 32px;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.82rem;
  outline: none;
  transition: all 0.2s ease;
}

.search-input:focus {
  border-color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.03);
  box-shadow: 0 0 12px rgba(0, 255, 198, 0.12);
}

/* Transacciones */
.transactions-container {
  min-height: 180px;
}

.transactions-rows {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeletons-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tx-skeleton {
  height: 60px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
}

.shimmer {
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.02) 25%, rgba(255, 255, 255, 0.06) 50%, rgba(255, 255, 255, 0.02) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.6s infinite;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 2.2rem;
  margin-bottom: 10px;
  opacity: 0.7;
}

.empty-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--hermes-text-primary, #F4F4F5);
  margin-bottom: 6px;
}

.empty-desc {
  font-size: 0.82rem;
  color: var(--hermes-text-muted, #94949E);
  margin-bottom: 16px;
  max-width: 320px;
}

/* Paginación */
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  flex-wrap: wrap;
  gap: 10px;
}

.page-info {
  font-size: 0.78rem;
  color: var(--hermes-text-muted, #94949E);
}

.page-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary, #F4F4F5);
  padding: 5px 12px;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.page-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.15);
}

.page-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.current-page-badge {
  font-size: 0.78rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(0, 255, 198, 0.08);
  color: var(--hermes-accent-teal, #00FFC6);
  border: 1px solid rgba(0, 255, 198, 0.2);
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
</style>

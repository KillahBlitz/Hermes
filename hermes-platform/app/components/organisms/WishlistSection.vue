<script setup lang="ts">
import { computed } from 'vue'
import type { WishlistItem, WishlistStats } from '~/composables/useLists'
import WishlistCard from '~/components/molecules/WishlistCard.vue'

const props = defineProps<{
  items: WishlistItem[]
  stats: WishlistStats
  filterStatus: string
  filterCategory: string
  filterPriority: string
  searchQuery: string
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'updateFilters', status: string, category: string, priority: string, search: string): void
  (e: 'toggleStatus', item: WishlistItem): void
  (e: 'editItem', item: WishlistItem): void
  (e: 'uploadPhoto', item: WishlistItem): void
  (e: 'deleteItem', item: WishlistItem): void
  (e: 'newItem'): void
}>()

const formattedPendingValue = computed(() => {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: props.stats.currency || 'MXN',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(props.stats.total_pending_value)
})

const formattedPurchasedValue = computed(() => {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: props.stats.currency || 'MXN',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(props.stats.total_purchased_value)
})
</script>

<template>
  <div class="wishlist-section-wrapper">
    <!-- Top KPIs Banner -->
    <div class="wishlist-kpis-grid">
      <div class="kpi-card glass-panel highlight-teal">
        <div class="kpi-icon">🎁</div>
        <div class="kpi-content">
          <span class="kpi-label">Deseos Pendientes</span>
          <span class="kpi-value text-accent-teal">{{ stats.pending_items }}</span>
        </div>
      </div>

      <div class="kpi-card glass-panel highlight-blue">
        <div class="kpi-icon">💰</div>
        <div class="kpi-content">
          <span class="kpi-label">Inversión Estimada Pendiente</span>
          <span class="kpi-value text-accent-blue">{{ formattedPendingValue }}</span>
        </div>
      </div>

      <div class="kpi-card glass-panel highlight-pink">
        <div class="kpi-icon">🏆</div>
        <div class="kpi-content">
          <span class="kpi-label">Deseos Cumplidos</span>
          <span class="kpi-value text-accent-pink">{{ stats.purchased_items }}</span>
          <span class="kpi-subtext">({{ formattedPurchasedValue }} adquiridos)</span>
        </div>
      </div>
    </div>

    <!-- Barra de Filtros y Búsqueda -->
    <div class="filters-toolbar glass-panel">
      <div class="toolbar-left">
        <!-- Filtro Estado -->
        <select
          :value="filterStatus"
          class="filter-select"
          @change="emit('updateFilters', ($event.target as HTMLSelectElement).value, filterCategory, filterPriority, searchQuery)"
        >
          <option value="">Todos los Estados</option>
          <option value="PENDING">Pendientes</option>
          <option value="PURCHASED">Comprados ✓</option>
          <option value="ARCHIVED">Descartados</option>
        </select>

        <!-- Filtro Prioridad -->
        <select
          :value="filterPriority"
          class="filter-select"
          @change="emit('updateFilters', filterStatus, filterCategory, ($event.target as HTMLSelectElement).value, searchQuery)"
        >
          <option value="">Todas las Prioridades</option>
          <option value="ALTA">🔥 Alta</option>
          <option value="MEDIA">⚡ Media</option>
          <option value="BAJA">💤 Baja</option>
        </select>

        <!-- Buscador -->
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input
            :value="searchQuery"
            type="text"
            placeholder="Buscar por nombre..."
            class="search-input"
            @input="emit('updateFilters', filterStatus, filterCategory, filterPriority, ($event.target as HTMLInputElement).value)"
          />
        </div>
      </div>

      <div class="toolbar-right">
        <button class="primary-btn glow-teal" @click="emit('newItem')">
          <span>+</span> Nuevo Deseo
        </button>
      </div>
    </div>

    <!-- Cuadrícula de Artículos -->
    <div class="wishlist-grid-container">
      <div v-if="loading" class="skeletons-grid">
        <div v-for="i in 4" :key="i" class="card-skeleton shimmer"></div>
      </div>

      <div v-else-if="items.length === 0" class="empty-state glass-panel">
        <span class="empty-icon">🎁</span>
        <h3 class="empty-title">Sin artículos en tu lista de deseos</h3>
        <p class="empty-desc">
          Registra compras futuras, gadgets, libros o herramientas que planeas adquirir y sube fotos a tu Google Drive.
        </p>
        <button class="primary-btn glow-teal" @click="emit('newItem')">
          + Agregar primer deseo
        </button>
      </div>

      <div v-else class="wishlist-cards-grid">
        <WishlistCard
          v-for="item in items"
          :key="item.id"
          :item="item"
          @toggle-status="emit('toggleStatus', item)"
          @edit="emit('editItem', item)"
          @upload-photo="emit('uploadPhoto', item)"
          @delete="emit('deleteItem', item)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.wishlist-section-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* KPIs */
.wishlist-kpis-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.kpi-card {
  padding: 18px 20px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(23, 23, 28, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.kpi-icon {
  font-size: 2rem;
}

.kpi-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.kpi-label {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--hermes-text-muted, #94949E);
}

.kpi-value {
  font-size: 1.4rem;
  font-weight: 800;
  font-family: 'JetBrains Mono', monospace;
  line-height: 1.2;
}

.kpi-subtext {
  font-size: 0.72rem;
  color: var(--hermes-text-muted, #94949E);
}

/* Toolbar */
.filters-toolbar {
  padding: 12px 18px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  flex-wrap: wrap;
}

.filter-select {
  background: rgba(23, 23, 28, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary, #F4F4F5);
  padding: 7px 12px;
  border-radius: 10px;
  font-size: 0.82rem;
  outline: none;
}

.filter-select option {
  background: #17171c;
  color: #F4F4F5;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 180px;
}

.search-icon {
  position: absolute;
  left: 10px;
  font-size: 0.78rem;
  opacity: 0.6;
  pointer-events: none;
}

.search-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 7px 12px 7px 30px;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.82rem;
  outline: none;
}

.primary-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  font-weight: 800;
  font-size: 0.85rem;
  padding: 8px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 16px rgba(0, 255, 198, 0.4);
}

/* Grid */
.wishlist-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
}

.skeletons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
}

.card-skeleton {
  height: 280px;
  border-radius: 16px;
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
  padding: 60px 20px;
  text-align: center;
  border-radius: 16px;
}

.empty-icon {
  font-size: 2.8rem;
  margin-bottom: 12px;
  color: var(--hermes-accent-teal, #00FFC6);
}

.empty-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 0.88rem;
  color: var(--hermes-text-muted, #94949E);
  max-width: 440px;
  margin-bottom: 20px;
  line-height: 1.5;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

@media (max-width: 900px) {
  .wishlist-kpis-grid {
    grid-template-columns: 1fr;
  }
}
</style>

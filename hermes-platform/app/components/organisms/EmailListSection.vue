<script setup lang="ts">
import { useGmailService } from '~/composables/useGmailService'
import EmailCard from '~/components/molecules/EmailCard.vue'
import EmailDetailModal from '~/components/organisms/EmailDetailModal.vue'
import DeleteConfirmModal from '~/components/organisms/DeleteConfirmModal.vue'

const { logout } = useAuth()
const {
  emails,
  loading,
  error,
  activeFilter,
  searchQuery,
  currentPage,
  hasNextPage,
  hasPrevPage,
  selectedEmail,
  isDetailOpen,
  detailLoading,
  emailToDelete,
  isDeleteModalOpen,
  isDeleting,
  fetchEmails,
  openEmailDetail,
  closeEmailDetail,
  promptDeleteEmail,
  cancelDelete,
  executeDeleteEmail,
  setFilter,
  setSearch,
  nextPage,
  prevPage
} = useGmailService()

const localSearch = ref('')
let searchTimeout: any = null

const handleSearchInput = (e: Event) => {
  const target = e.target as HTMLInputElement
  localSearch.value = target.value
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    setSearch(localSearch.value)
  }, 400)
}

onMounted(() => {
  if (emails.value.length === 0) {
    fetchEmails(1)
  }
})
</script>

<template>
  <section class="email-section">
    <!-- Toolbar: Filters + Search + Refresh -->
    <div class="email-toolbar glass-panel">
      <!-- Filter Chips -->
      <div class="filter-chips">
        <button
          class="chip-btn"
          :class="{ active: activeFilter === 'all' }"
          type="button"
          @click="setFilter('all')"
        >
          Todos los Prioritarios
        </button>
        <button
          class="chip-btn"
          :class="{ active: activeFilter === 'starred' }"
          type="button"
          @click="setFilter('starred')"
        >
          ⭐ Destacados
        </button>
        <button
          class="chip-btn"
          :class="{ active: activeFilter === 'important' }"
          type="button"
          @click="setFilter('important')"
        >
          🏷️ Importantes
        </button>
      </div>

      <!-- Right Controls: Search + Refresh -->
      <div class="toolbar-right">
        <div class="search-input-box">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <input
            v-model="localSearch"
            type="text"
            placeholder="Buscar por remitente, asunto..."
            class="search-field"
            @input="handleSearchInput"
          />
        </div>

        <button
          class="refresh-btn"
          :disabled="loading"
          title="Actualizar correos"
          type="button"
          @click="fetchEmails(currentPage)"
        >
          <svg :class="{ spinning: loading }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10" />
            <polyline points="1 20 1 14 7 14" />
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Error Banner with Action -->
    <div v-if="error" class="alert-error-neon">
      <div class="error-icon-box">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
      </div>
      <div class="error-body">
        <strong class="error-title">No se pudieron sincronizar los correos de Gmail</strong>
        <p class="error-desc">{{ error }}</p>
        <div class="error-actions">
          <button class="btn-error-action" type="button" @click="fetchEmails(1)">
            🔄 Reintentar
          </button>
          <button class="btn-error-action btn-error-logout" type="button" @click="logout">
            🔑 Volver a iniciar sesión
          </button>
        </div>
      </div>
    </div>

    <!-- Loading Skeleton List -->
    <div v-if="loading && emails.length === 0" class="emails-skeleton-list">
      <div v-for="n in 5" :key="n" class="skeleton-card glass-panel shimmer" />
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && emails.length === 0" class="empty-state glass-panel">
      <div class="empty-icon-circle">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
          <polyline points="22,6 12,13 2,6" />
        </svg>
      </div>
      <h3 class="empty-title">No hay correos en esta vista</h3>
      <p class="empty-desc">
        No se encontraron correos para el filtro o página seleccionada.
      </p>
    </div>

    <!-- Email List & Pagination -->
    <div v-else class="emails-content-wrapper">
      <div class="emails-list-container">
        <EmailCard
          v-for="email in emails"
          :key="email.id"
          :email="email"
          @click="openEmailDetail(email.id)"
          @delete="promptDeleteEmail(email)"
        />
      </div>

      <!-- Pagination Controls (10 in 10) -->
      <div class="email-pagination-bar glass-panel">
        <div class="pagination-info">
          <span class="info-badge">10 por página</span>
        </div>

        <div class="pagination-controls">
          <button
            class="btn-page-nav"
            :disabled="!hasPrevPage || loading"
            type="button"
            @click="prevPage"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="15 18 9 12 15 6" />
            </svg>
            Anterior
          </button>

          <div class="page-indicator">
            Página <span class="page-number-highlight">{{ currentPage }}</span>
          </div>

          <button
            class="btn-page-nav"
            :disabled="!hasNextPage || loading"
            type="button"
            @click="nextPage"
          >
            Siguiente
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Detail Modal -->
    <EmailDetailModal
      :is-open="isDetailOpen"
      :email="selectedEmail"
      :loading="detailLoading"
      @close="closeEmailDetail"
      @delete="selectedEmail ? promptDeleteEmail(selectedEmail) : null"
    />

    <!-- Delete Confirmation Modal -->
    <DeleteConfirmModal
      :is-open="isDeleteModalOpen"
      title="Eliminar correo de Gmail"
      message="¿Estás seguro de que deseas enviar este correo a la papelera de Gmail? Esta acción se registrará en la bitácora de auditoría."
      :item-title="emailToDelete?.subject"
      :is-deleting="isDeleting"
      @confirm="executeDeleteEmail"
      @cancel="cancelDelete"
    />
  </section>
</template>

<style scoped>
.email-section {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.email-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  border-radius: 14px;
  flex-wrap: wrap;
  gap: 12px;
}

.filter-chips {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chip-btn {
  padding: 6px 14px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted);
  font-family: inherit;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chip-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary);
}

.chip-btn.active {
  background: rgba(0, 229, 255, 0.15);
  border-color: rgba(0, 229, 255, 0.4);
  color: var(--hermes-accent-blue);
  box-shadow: 0 0 12px rgba(0, 229, 255, 0.2);
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-input-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 6px 12px;
  width: 260px;
  transition: border-color 0.2s ease;
}

.search-input-box:focus-within {
  border-color: var(--hermes-accent-blue);
  box-shadow: 0 0 12px rgba(0, 229, 255, 0.15);
}

.search-icon {
  color: var(--hermes-text-muted);
  flex-shrink: 0;
}

.search-field {
  background: transparent;
  border: none;
  color: var(--hermes-text-primary);
  font-family: inherit;
  font-size: 0.84rem;
  width: 100%;
  outline: none;
}

.search-field::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.refresh-btn {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover:not(:disabled) {
  color: var(--hermes-accent-blue);
  background: rgba(0, 229, 255, 0.1);
  border-color: rgba(0, 229, 255, 0.3);
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.alert-error-neon {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px 20px;
  border-radius: 14px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.35);
  color: #FCA5A5;
}

.error-icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #EF4444;
  margin-top: 2px;
  flex-shrink: 0;
}

.error-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.error-title {
  color: #FECACA;
  font-size: 0.95rem;
  font-weight: 700;
}

.error-desc {
  margin: 0;
  font-size: 0.86rem;
  line-height: 1.5;
  color: #FCA5A5;
}

.error-actions {
  display: flex;
  gap: 10px;
  margin-top: 6px;
  flex-wrap: wrap;
}

.btn-error-action {
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #ffffff;
  transition: all 0.2s ease;
  font-family: inherit;
}

.btn-error-action:hover {
  background: rgba(255, 255, 255, 0.16);
  transform: translateY(-1px);
}

.btn-error-logout {
  background: rgba(255, 0, 127, 0.2);
  border-color: rgba(255, 0, 127, 0.4);
  color: #ffffff;
}

.btn-error-logout:hover {
  background: rgba(255, 0, 127, 0.35);
}

.emails-content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.emails-list-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* ── Pagination Bar ── */
.email-pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  flex-wrap: wrap;
  gap: 12px;
}

.pagination-info {
  display: flex;
  align-items: center;
}

.info-badge {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--hermes-accent-teal);
  background: rgba(0, 255, 198, 0.08);
  border: 1px solid rgba(0, 255, 198, 0.2);
  padding: 4px 10px;
  border-radius: 6px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-page-nav {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary);
  font-family: inherit;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-page-nav:hover:not(:disabled) {
  background: rgba(0, 229, 255, 0.12);
  border-color: rgba(0, 229, 255, 0.35);
  color: var(--hermes-accent-blue);
  transform: translateY(-1px);
}

.btn-page-nav:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.page-indicator {
  font-size: 0.86rem;
  color: var(--hermes-text-muted);
  font-weight: 500;
}

.page-number-highlight {
  color: var(--hermes-accent-blue);
  font-weight: 800;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  border-radius: 16px;
  text-align: center;
}

.empty-icon-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--hermes-text-muted);
  margin-bottom: 16px;
}

.empty-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
  margin: 0 0 6px 0;
}

.empty-desc {
  font-size: 0.88rem;
  color: var(--hermes-text-muted);
  max-width: 400px;
  margin: 0;
}

/* Skeleton loader */
.emails-skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton-card {
  height: 84px;
  border-radius: 14px;
}

.shimmer {
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.02) 25%, rgba(255, 255, 255, 0.06) 50%, rgba(255, 255, 255, 0.02) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>

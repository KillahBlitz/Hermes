<script setup lang="ts">
defineProps<{
  isOpen: boolean
  title?: string
  message?: string
  itemTitle?: string
  isDeleting?: boolean
}>()

const emit = defineEmits<{
  (e: 'confirm'): void
  (e: 'cancel'): void
}>()
</script>

<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isOpen" class="modal-backdrop" @click="emit('cancel')">
        <div class="delete-modal glass-panel" @click.stop>
          <!-- Warning Icon Header -->
          <div class="modal-icon-warning">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
              <line x1="12" y1="9" x2="12" y2="13" />
              <line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
          </div>

          <h3 class="modal-title">{{ title || 'Confirmar eliminación' }}</h3>
          <p class="modal-message">{{ message || '¿Estás seguro de que deseas enviar este elemento a la papelera?' }}</p>

          <div v-if="itemTitle" class="item-preview-box">
            <span class="item-title-text">{{ itemTitle }}</span>
          </div>

          <div class="modal-actions">
            <button
              class="btn-modal btn-cancel"
              type="button"
              :disabled="isDeleting"
              @click="emit('cancel')"
            >
              Cancelar
            </button>
            <button
              class="btn-modal btn-delete"
              type="button"
              :disabled="isDeleting"
              @click="emit('confirm')"
            >
              <svg v-if="isDeleting" class="spinner-inline" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6" />
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              </svg>
              {{ isDeleting ? 'Eliminando...' : 'Sí, eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.delete-modal {
  width: 100%;
  max-width: 440px;
  padding: 28px;
  border-radius: 18px;
  border: 1px solid rgba(255, 0, 127, 0.3);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.6), 0 0 30px rgba(255, 0, 127, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.modal-icon-warning {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(255, 0, 127, 0.12);
  border: 1px solid rgba(255, 0, 127, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--hermes-accent-pink);
  margin-bottom: 16px;
  animation: pulse-warning 2s infinite ease-in-out;
}

@keyframes pulse-warning {
  0%, 100% { box-shadow: 0 0 0 0 rgba(255, 0, 127, 0.4); }
  50% { box-shadow: 0 0 0 12px rgba(255, 0, 127, 0); }
}

.modal-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
  margin: 0 0 8px 0;
}

.modal-message {
  font-size: 0.88rem;
  color: var(--hermes-text-muted);
  line-height: 1.5;
  margin: 0 0 16px 0;
}

.item-preview-box {
  width: 100%;
  padding: 10px 14px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  margin-bottom: 24px;
  max-height: 60px;
  overflow: hidden;
}

.item-title-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #E4E4E7;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.modal-actions {
  display: flex;
  gap: 12px;
  width: 100%;
}

.btn-modal {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 11px 18px;
  border-radius: 10px;
  font-family: inherit;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted);
}

.btn-cancel:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.12);
  color: var(--hermes-text-primary);
}

.btn-delete {
  background: linear-gradient(135deg, rgba(255, 0, 127, 0.8), rgba(220, 38, 38, 0.8));
  border: 1px solid var(--hermes-accent-pink);
  color: #ffffff;
  box-shadow: 0 0 16px rgba(255, 0, 127, 0.3);
}

.btn-delete:hover:not(:disabled) {
  background: linear-gradient(135deg, #FF007F, #DC2626);
  box-shadow: 0 0 24px rgba(255, 0, 127, 0.5);
  transform: translateY(-1px);
}

.btn-modal:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-inline {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── Modal Transition ── */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>

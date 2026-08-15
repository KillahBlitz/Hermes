<script setup lang="ts">
import type { EmailDetail } from '~/composables/useGmailService'

const props = defineProps<{
  isOpen: boolean
  email: EmailDetail | null
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'delete'): void
}>()

const formattedDate = computed(() => {
  if (!props.email?.date) return ''
  try {
    const d = new Date(props.email.date)
    return d.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return props.email.date
  }
})

const formatFileSize = (bytes: number) => {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}
</script>

<template>
  <Teleport to="body">
    <Transition name="modal-slide">
      <div v-if="isOpen" class="modal-backdrop" @click="emit('close')">
        <div class="email-detail-container glass-panel" @click.stop>
          <!-- Header Bar -->
          <div class="modal-top-bar">
            <div class="top-bar-left">
              <span class="service-tag">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                  <polyline points="22,6 12,13 2,6" />
                </svg>
                Gmail
              </span>
              <span v-if="email?.labels.includes('STARRED')" class="badge-pill badge-gold">⭐ Destacado</span>
              <span v-if="email?.labels.includes('IMPORTANT')" class="badge-pill badge-cyan">🏷️ Importante</span>
            </div>

            <div class="top-bar-right">
              <button
                v-if="email"
                class="btn-icon-action btn-trash"
                title="Eliminar este correo"
                type="button"
                @click="emit('delete')"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6" />
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                </svg>
              </button>
              <button
                class="btn-icon-action btn-close"
                title="Cerrar ventana"
                type="button"
                @click="emit('close')"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="detail-loading-box">
            <div class="spinner-neon" />
            <p class="loading-text">Cargando contenido del correo...</p>
          </div>

          <!-- Email Content -->
          <div v-else-if="email" class="email-scroll-content">
            <!-- Subject & Meta -->
            <div class="email-meta-section">
              <h2 class="email-subject-title">{{ email.subject }}</h2>

              <div class="email-sender-card">
                <div class="sender-avatar-large">
                  {{ (email.sender || email.sender_email || 'U').charAt(0).toUpperCase() }}
                </div>
                <div class="sender-info-box">
                  <div class="sender-primary-line">
                    <span class="sender-display">{{ email.sender }}</span>
                    <span class="sender-email-text">&lt;{{ email.sender_email }}&gt;</span>
                  </div>
                  <div class="recipient-line">
                    Para: <span class="recipient-value">{{ email.recipients || 'mí' }}</span>
                  </div>
                </div>
                <div class="email-exact-date">
                  {{ formattedDate }}
                </div>
              </div>
            </div>

            <!-- Email Body -->
            <div class="email-body-section">
              <!-- Render HTML body if present, else plaintext -->
              <div
                v-if="email.body_html"
                class="email-html-wrapper"
                v-html="email.body_html"
              />
              <pre v-else class="email-plaintext-wrapper">{{ email.body_text || '(Mensaje sin contenido de texto)' }}</pre>
            </div>

            <!-- Attachments -->
            <div v-if="email.attachments && email.attachments.length > 0" class="email-attachments-section">
              <h4 class="attachments-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
                </svg>
                Archivos Adjuntos ({{ email.attachments.length }})
              </h4>
              <div class="attachments-grid">
                <div
                  v-for="att in email.attachments"
                  :key="att.attachment_id"
                  class="attachment-card"
                >
                  <div class="att-icon">📎</div>
                  <div class="att-info">
                    <span class="att-name" :title="att.filename">{{ att.filename }}</span>
                    <span class="att-size">{{ formatFileSize(att.size) }}</span>
                  </div>
                </div>
              </div>
            </div>
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
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 24px;
}

.email-detail-container {
  width: 100%;
  max-width: 860px;
  height: 85vh;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
}

.modal-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(0, 0, 0, 0.2);
}

.top-bar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.service-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--hermes-accent-blue);
  background: rgba(0, 229, 255, 0.1);
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid rgba(0, 229, 255, 0.2);
}

.badge-pill {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
}

.badge-gold {
  background: rgba(245, 158, 11, 0.15);
  color: #FBBF24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.badge-cyan {
  background: rgba(0, 229, 255, 0.12);
  color: var(--hermes-accent-blue);
  border: 1px solid rgba(0, 229, 255, 0.25);
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-icon-action {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-icon-action:hover {
  color: var(--hermes-text-primary);
  background: rgba(255, 255, 255, 0.1);
}

.btn-trash:hover {
  background: rgba(255, 0, 127, 0.15);
  border-color: rgba(255, 0, 127, 0.4);
  color: var(--hermes-accent-pink);
}

.btn-close:hover {
  transform: scale(1.08);
}

.detail-loading-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.spinner-neon {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(0, 229, 255, 0.2);
  border-top-color: var(--hermes-accent-blue);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 0.9rem;
  color: var(--hermes-text-muted);
}

.email-scroll-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.email-subject-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--hermes-text-primary);
  margin: 0 0 16px 0;
  line-height: 1.3;
}

.email-sender-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.sender-avatar-large {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--hermes-accent-blue), var(--hermes-accent-pink));
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.sender-info-box {
  flex: 1;
  min-width: 0;
}

.sender-primary-line {
  display: flex;
  align-items: baseline;
  gap: 8px;
  flex-wrap: wrap;
}

.sender-display {
  font-weight: 700;
  color: var(--hermes-text-primary);
  font-size: 0.95rem;
}

.sender-email-text {
  font-size: 0.82rem;
  color: var(--hermes-text-muted);
}

.recipient-line {
  font-size: 0.78rem;
  color: var(--hermes-text-muted);
  margin-top: 2px;
}

.recipient-value {
  color: #D4D4D8;
}

.email-exact-date {
  font-size: 0.8rem;
  color: var(--hermes-text-muted);
  flex-shrink: 0;
  text-align: right;
}

.email-body-section {
  padding: 16px;
  background: rgba(0, 0, 0, 0.25);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.04);
  color: #E4E4E7;
  font-size: 0.92rem;
  line-height: 1.6;
  min-height: 180px;
}

.email-html-wrapper {
  overflow-x: auto;
  color: #E4E4E7;
}

.email-html-wrapper :deep(a) {
  color: var(--hermes-accent-blue);
}

.email-plaintext-wrapper {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: inherit;
  margin: 0;
  color: #D4D4D8;
}

.email-attachments-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.attachments-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--hermes-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0;
}

.attachments-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.attachment-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 8px;
  max-width: 240px;
}

.att-icon { font-size: 1.1rem; }
.att-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.att-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--hermes-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.att-size {
  font-size: 0.72rem;
  color: var(--hermes-text-muted);
}

/* ── Transitions ── */
.modal-slide-enter-active,
.modal-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-slide-enter-from,
.modal-slide-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.98);
}
</style>

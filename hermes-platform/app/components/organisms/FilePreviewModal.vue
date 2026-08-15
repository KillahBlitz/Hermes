<script setup lang="ts">
import type { DriveFile, PreviewInfo } from '~/composables/useDriveBucket'

const props = defineProps<{
  isOpen: boolean
  file: DriveFile | null
  previewInfo: PreviewInfo | null
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const fileCategory = computed(() => {
  if (!props.file) return 'file'
  const mime = props.file.mime_type?.toLowerCase() || ''
  if (mime.startsWith('image/')) return 'image'
  if (mime.startsWith('video/')) return 'video'
  if (mime.startsWith('audio/')) return 'audio'
  if (mime.includes('pdf')) return 'pdf'
  return 'doc'
})

const previewUrl = computed(() => {
  if (props.previewInfo?.web_view_link) {
    // Replace /view with /preview for cleaner embed iframe
    return props.previewInfo.web_view_link.replace(/\/view(\?.*)?$/, '/preview')
  }
  return ''
})

const directDownloadUrl = computed(() => {
  return props.previewInfo?.web_content_link || props.previewInfo?.web_view_link || '#'
})
</script>

<template>
  <Teleport to="body">
    <Transition name="modal-slide">
      <div v-if="isOpen" class="modal-backdrop" @click="emit('close')">
        <div class="preview-container glass-panel" @click.stop>
          <!-- Modal Header -->
          <div class="modal-top-bar">
            <div class="file-title-group">
              <span class="service-tag">Drive Bucket</span>
              <h3 class="file-name-header" :title="file?.name">{{ file?.name }}</h3>
            </div>

            <div class="top-bar-actions">
              <a
                v-if="directDownloadUrl !== '#'"
                :href="directDownloadUrl"
                target="_blank"
                class="btn-icon-action btn-download"
                title="Abrir en Google Drive / Descargar"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
              </a>
              <button
                class="btn-icon-action btn-close"
                title="Cerrar vista previa"
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

          <!-- Modal Body Content -->
          <div class="preview-body">
            <!-- Loading State -->
            <div v-if="loading" class="preview-loading-box">
              <div class="spinner-neon" />
              <p class="loading-text">Cargando vista previa interactiva...</p>
            </div>

            <!-- Image View -->
            <div v-else-if="fileCategory === 'image'" class="image-preview-wrapper">
              <img
                :src="previewInfo?.thumbnail_link || previewUrl"
                :alt="file?.name"
                class="preview-image-full"
              />
            </div>

            <!-- Video Player (HTML5 / Drive Embed) -->
            <div v-else-if="fileCategory === 'video'" class="video-preview-wrapper">
              <iframe
                v-if="previewUrl"
                :src="previewUrl"
                class="preview-iframe"
                allow="autoplay"
                allowfullscreen
              />
              <p v-else class="preview-fallback-text">No se pudo cargar el reproductor de video.</p>
            </div>

            <!-- PDF / Documents Embed Iframe -->
            <div v-else-if="fileCategory === 'pdf' || fileCategory === 'doc'" class="doc-preview-wrapper">
              <iframe
                v-if="previewUrl"
                :src="previewUrl"
                class="preview-iframe"
                allowfullscreen
              />
              <div v-else class="preview-fallback-box">
                <p>Este archivo no tiene una vista previa incrustada disponible.</p>
                <a :href="directDownloadUrl" target="_blank" class="btn-download-direct">
                  Abrir en Google Drive
                </a>
              </div>
            </div>

            <!-- Generic / Audio -->
            <div v-else class="generic-preview-wrapper">
              <div class="generic-icon-box">📁</div>
              <p class="generic-name">{{ file?.name }}</p>
              <a :href="directDownloadUrl" target="_blank" class="btn-download-direct">
                Descargar o ver en Google Drive
              </a>
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
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 24px;
}

.preview-container {
  width: 100%;
  max-width: 960px;
  height: 85vh;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.8);
}

.modal-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(0, 0, 0, 0.3);
}

.file-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.service-tag {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--hermes-accent-teal);
  background: rgba(0, 255, 198, 0.1);
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid rgba(0, 255, 198, 0.2);
  flex-shrink: 0;
}

.file-name-header {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.top-bar-actions {
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
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-icon-action:hover {
  color: var(--hermes-text-primary);
  background: rgba(255, 255, 255, 0.1);
}

.btn-download:hover {
  color: var(--hermes-accent-blue);
  border-color: rgba(0, 229, 255, 0.3);
}

.preview-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.4);
  position: relative;
  overflow: hidden;
}

.preview-loading-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}

.spinner-neon {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(0, 255, 198, 0.2);
  border-top-color: var(--hermes-accent-teal);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 0.88rem;
  color: var(--hermes-text-muted);
}

.image-preview-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.preview-image-full {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.video-preview-wrapper,
.doc-preview-wrapper {
  width: 100%;
  height: 100%;
}

.preview-iframe {
  width: 100%;
  height: 100%;
  border: none;
  background: #111114;
}

.generic-preview-wrapper,
.preview-fallback-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px;
  text-align: center;
}

.generic-icon-box {
  font-size: 3.5rem;
}

.generic-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--hermes-text-primary);
  margin: 0;
}

.btn-download-direct {
  padding: 10px 20px;
  background: linear-gradient(135deg, var(--hermes-accent-blue), var(--hermes-accent-pink));
  color: #ffffff;
  font-weight: 600;
  font-size: 0.9rem;
  border-radius: 10px;
  text-decoration: none;
  transition: transform 0.2s ease;
}

.btn-download-direct:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.4);
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

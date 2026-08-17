<script setup lang="ts">
import { ref } from 'vue'
import type { WishlistItem } from '~/composables/useLists'
import { useDriveBucket } from '~/composables/useDriveBucket'

const props = defineProps<{
  show: boolean
  item: WishlistItem | null
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'upload', file: File): void
}>()

const { getDriveFileContentUrl } = useDriveBucket()
const isDragging = ref(false)
const selectedFile = ref<File | null>(null)
const previewUrl = ref<string | null>(null)

const getImgSrc = (img: { drive_file_id?: string; thumbnail_link?: string; web_view_link?: string }) => {
  if (img.drive_file_id) {
    return getDriveFileContentUrl(img.drive_file_id) || img.thumbnail_link || img.web_view_link || ''
  }
  return img.thumbnail_link || img.web_view_link || ''
}

const onFileSelected = (e: Event) => {
  const input = e.target as HTMLInputElement
  if (input.files && input.files[0]) {
    setFile(input.files[0])
  }
}

const onDrop = (e: DragEvent) => {
  isDragging.value = false
  if (e.dataTransfer?.files && e.dataTransfer.files[0]) {
    setFile(e.dataTransfer.files[0])
  }
}

const setFile = (file: File) => {
  selectedFile.value = file
  if (file.type.startsWith('image/')) {
    previewUrl.value = URL.createObjectURL(file)
  }
}

const handleUpload = () => {
  if (!selectedFile.value) return
  emit('upload', selectedFile.value)
  selectedFile.value = null
  previewUrl.value = null
}
</script>

<template>
  <div v-if="show && item" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <div class="modal-header">
        <div class="modal-title-group">
          <h3 class="modal-title">Fotos en Google Drive</h3>
          <span class="modal-subtitle">Almacenamiento seguro en tu carpeta <code>hermes/whitelist</code></span>
        </div>
        <button class="close-btn" @click="emit('close')">✕</button>
      </div>

      <!-- Artículo Info -->
      <div class="item-summary-badge">
        <span class="item-name">🛍️ {{ item.name }}</span>
      </div>

      <!-- Galería de fotos existentes en Drive -->
      <div v-if="item.images.length > 0" class="existing-photos-section">
        <h4 class="section-subtitle">Fotos guardadas en Drive ({{ item.images.length }})</h4>
        <div class="existing-photos-grid">
          <a
            v-for="img in item.images"
            :key="img.drive_file_id"
            :href="img.web_view_link"
            target="_blank"
            rel="noopener noreferrer"
            class="drive-photo-card"
            title="Ver en Google Drive"
          >
            <img :src="getImgSrc(img)" :alt="img.name" class="drive-thumb" />
            <span class="photo-name">{{ img.name }}</span>
          </a>
        </div>
      </div>

      <!-- Dropzone para nueva foto -->
      <div
        class="dropzone-box"
        :class="{ dragging: isDragging }"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="onDrop"
      >
        <div v-if="previewUrl" class="local-preview-box">
          <img :src="previewUrl" alt="Vista previa" class="local-thumb" />
          <span class="selected-filename">{{ selectedFile?.name }}</span>
        </div>

        <div v-else class="dropzone-prompt">
          <span class="cloud-icon">☁️</span>
          <p class="dropzone-text">Arrastra una imagen aquí o selecciónala de tu equipo</p>
          <label class="browse-file-btn glow-teal">
            <span>Explorar archivo</span>
            <input type="file" accept="image/*" class="d-none" @change="onFileSelected" />
          </label>
        </div>
      </div>

      <!-- Footer -->
      <div class="modal-footer">
        <button type="button" class="cancel-btn" @click="emit('close')">
          Cerrar
        </button>
        <button
          v-if="selectedFile"
          type="button"
          class="submit-btn glow-teal"
          :disabled="loading"
          @click="handleUpload"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          Subir a Drive (hermes/whitelist)
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  animation: fadeIn 0.15s ease-out;
}

.modal-card {
  width: 100%;
  max-width: 540px;
  border-radius: 20px;
  padding: 24px;
  background: rgba(23, 23, 28, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-top: 3px solid var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
  animation: scaleUp 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0 0 4px 0;
}

.modal-subtitle {
  font-size: 0.8rem;
  color: var(--hermes-text-muted, #94949E);
}

.modal-subtitle code {
  color: var(--hermes-accent-teal, #00FFC6);
}

.close-btn {
  background: rgba(255, 255, 255, 0.05);
  border: none;
  color: var(--hermes-text-muted, #94949E);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-summary-badge {
  padding: 8px 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 16px;
}

.item-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--hermes-text-primary, #F4F4F5);
}

/* Fotos existentes */
.existing-photos-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.section-subtitle {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--hermes-text-muted, #94949E);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin: 0;
}

.existing-photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
  max-height: 140px;
  overflow-y: auto;
}

.drive-photo-card {
  position: relative;
  height: 80px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  text-decoration: none;
  background: #0c0c0e;
}

.drive-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-name {
  position: absolute;
  bottom: 0;
  inset-inline: 0;
  background: rgba(0, 0, 0, 0.7);
  font-size: 0.65rem;
  color: #fff;
  padding: 2px 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Dropzone */
.dropzone-box {
  border: 2px dashed rgba(255, 255, 255, 0.15);
  border-radius: 14px;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: rgba(255, 255, 255, 0.02);
  transition: all 0.2s ease;
}

.dropzone-box.dragging {
  border-color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.05);
}

.dropzone-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.cloud-icon { font-size: 2.2rem; }

.dropzone-text {
  font-size: 0.82rem;
  color: var(--hermes-text-muted, #94949E);
  margin: 0;
}

.browse-file-btn {
  background: rgba(0, 229, 255, 0.15);
  border: 1px solid rgba(0, 229, 255, 0.35);
  color: var(--hermes-accent-blue, #00E5FF);
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  margin-top: 4px;
}

.d-none { display: none; }

.local-preview-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.local-thumb {
  max-height: 120px;
  border-radius: 10px;
}

.selected-filename {
  font-size: 0.78rem;
  color: var(--hermes-text-primary, #F4F4F5);
  font-family: 'JetBrains Mono', monospace;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.cancel-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted, #94949E);
  padding: 8px 16px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  padding: 8px 20px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 0.88rem;
  cursor: pointer;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
</style>

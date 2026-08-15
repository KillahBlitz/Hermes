<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    uploading?: boolean
    progress?: number
  }>(),
  {
    uploading: false,
    progress: 0
  }
)

const emit = defineEmits<{
  (e: 'file-selected', file: File): void
}>()

const isDragging = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) {
    emit('file-selected', file)
  }
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    emit('file-selected', file)
    target.value = ''
  }
}
</script>

<template>
  <div
    class="file-upload-zone"
    :class="{ 'is-dragging': isDragging, 'is-uploading': uploading }"
    @dragover="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
    @click="triggerFileInput"
  >
    <input
      ref="fileInput"
      type="file"
      class="hidden-input"
      @change="handleFileChange"
    />

    <!-- Upload in progress state -->
    <div v-if="uploading" class="upload-progress-state">
      <div class="spinner-neon" />
      <span class="upload-title">Subiendo archivo a Google Drive...</span>
      <div class="progress-bar-container">
        <div class="progress-bar-fill" :style="{ width: `${progress}%` }" />
      </div>
      <span class="progress-pct">{{ progress }}%</span>
    </div>

    <!-- Idle drag & drop state -->
    <div v-else class="upload-idle-state">
      <div class="upload-icon-circle">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="17 8 12 3 7 8" />
          <line x1="12" y1="3" x2="12" y2="15" />
        </svg>
      </div>
      <div class="upload-text-group">
        <p class="upload-main-text">
          <span class="highlight-text">Arrastra un archivo aquí</span> o haz clic para seleccionar
        </p>
        <p class="upload-sub-text">Cualquier tipo de archivo (imágenes, videos, documentos, comprimidos)</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.file-upload-zone {
  border: 2px dashed rgba(255, 255, 255, 0.12);
  border-radius: 14px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.02);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.file-upload-zone:hover {
  border-color: rgba(0, 229, 255, 0.4);
  background: rgba(0, 229, 255, 0.03);
}

.file-upload-zone.is-dragging {
  border-color: var(--hermes-accent-teal);
  background: rgba(0, 255, 198, 0.06);
  transform: scale(1.01);
  box-shadow: 0 0 24px rgba(0, 255, 198, 0.2);
}

.file-upload-zone.is-uploading {
  pointer-events: none;
  border-color: var(--hermes-accent-blue);
}

.hidden-input {
  display: none;
}

.upload-idle-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.upload-icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--hermes-accent-blue);
  transition: transform 0.25s ease;
}

.file-upload-zone:hover .upload-icon-circle {
  transform: translateY(-2px) scale(1.05);
}

.upload-text-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.upload-main-text {
  margin: 0;
  font-size: 0.92rem;
  color: var(--hermes-text-primary);
  font-weight: 500;
}

.highlight-text {
  color: var(--hermes-accent-blue);
  font-weight: 700;
}

.upload-sub-text {
  margin: 0;
  font-size: 0.78rem;
  color: var(--hermes-text-muted);
}

/* ── Progress State ── */
.upload-progress-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.spinner-neon {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(0, 229, 255, 0.2);
  border-top-color: var(--hermes-accent-blue);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.upload-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--hermes-text-primary);
}

.progress-bar-container {
  width: 240px;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--hermes-accent-blue), var(--hermes-accent-pink));
  transition: width 0.3s ease;
  border-radius: 3px;
}

.progress-pct {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--hermes-accent-blue);
}
</style>

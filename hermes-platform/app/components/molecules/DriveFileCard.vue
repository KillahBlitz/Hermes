<script setup lang="ts">
import type { DriveFile, StorageSource } from '~/composables/useDriveBucket'
import { useDriveBucket } from '~/composables/useDriveBucket'
import FileTypeIcon from '~/components/atoms/FileTypeIcon.vue'

const props = withDefaults(
  defineProps<{
    file: DriveFile
    viewMode?: 'grid' | 'list'
    source?: StorageSource
  }>(),
  {
    viewMode: 'grid',
    source: 'drive'
  }
)

const emit = defineEmits<{
  (e: 'click'): void
  (e: 'delete'): void
}>()

const { getFileContentUrl } = useDriveBucket()
const imageLoadError = ref(false)

const formattedSize = computed(() => {
  if (!props.file.size || props.file.is_folder) return ''
  const bytes = parseInt(props.file.size)
  if (isNaN(bytes)) return ''
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
})

const isImage = computed(() => {
  return props.file.mime_type?.startsWith('image/')
})

const imageSrc = computed(() => {
  if (imageLoadError.value || !isImage.value) return ''
  return getFileContentUrl(props.file.id, props.source) || props.file.thumbnail_url || ''
})
</script>

<template>
  <div
    class="drive-file-card glass-panel"
    :class="[viewMode, { 'is-folder': file.is_folder }]"
    @click="emit('click')"
  >
    <!-- Grid Thumbnail/Icon View -->
    <div v-if="viewMode === 'grid'" class="file-preview-area">
      <img
        v-if="isImage && imageSrc && !imageLoadError"
        :src="imageSrc"
        :alt="file.name"
        class="image-thumb"
        loading="lazy"
        @error="imageLoadError = true"
      />
      <div v-else class="icon-thumb-wrapper">
        <FileTypeIcon :mime-type="file.mime_type" :is-folder="file.is_folder" :size="40" />
      </div>
    </div>

    <!-- List Icon -->
    <div v-else class="list-icon-wrapper">
      <FileTypeIcon :mime-type="file.mime_type" :is-folder="file.is_folder" :size="20" />
    </div>

    <!-- File Info -->
    <div class="file-info">
      <div class="file-name" :title="file.name">{{ file.name }}</div>
      <div v-if="formattedSize || file.is_folder" class="file-meta">
        {{ file.is_folder ? 'Carpeta' : formattedSize }}
      </div>
    </div>

    <!-- Delete Action Button -->
    <button
      class="delete-file-btn"
      title="Eliminar archivo"
      type="button"
      @click.stop="emit('delete')"
    >
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="3 6 5 6 21 6" />
        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
      </svg>
    </button>
  </div>
</template>

<style scoped>
.drive-file-card {
  border-radius: 12px;
  cursor: pointer;
  position: relative;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.drive-file-card:hover {
  border-color: rgba(0, 229, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

.drive-file-card.is-folder:hover {
  border-color: rgba(245, 158, 11, 0.4);
}

/* ── Grid Mode ── */
.drive-file-card.grid {
  display: flex;
  flex-direction: column;
  padding: 12px;
  height: 160px;
}

.file-preview-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 10px;
  position: relative;
}

.image-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.icon-thumb-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.drive-file-card.grid .file-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.drive-file-card.grid .file-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--hermes-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.drive-file-card.grid .file-meta {
  font-size: 0.75rem;
  color: var(--hermes-text-muted);
}

/* ── List Mode ── */
.drive-file-card.list {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 16px;
}

.list-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.drive-file-card.list .file-info {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-width: 0;
}

.drive-file-card.list .file-name {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--hermes-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.drive-file-card.list .file-meta {
  font-size: 0.78rem;
  color: var(--hermes-text-muted);
  flex-shrink: 0;
  margin-left: 12px;
}

/* ── Delete Button ── */
.delete-file-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s ease;
  backdrop-filter: blur(8px);
}

.drive-file-card:hover .delete-file-btn {
  opacity: 1;
}

.delete-file-btn:hover {
  background: rgba(255, 0, 127, 0.2);
  border-color: rgba(255, 0, 127, 0.5);
  color: var(--hermes-accent-pink);
  transform: scale(1.1);
}
</style>

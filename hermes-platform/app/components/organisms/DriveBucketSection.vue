<script setup lang="ts">
import { useDriveBucket } from '~/composables/useDriveBucket'
import DriveBreadcrumb from '~/components/molecules/DriveBreadcrumb.vue'
import DriveFileCard from '~/components/molecules/DriveFileCard.vue'
import FileUploadZone from '~/components/molecules/FileUploadZone.vue'
import FilePreviewModal from '~/components/organisms/FilePreviewModal.vue'
import DeleteConfirmModal from '~/components/organisms/DeleteConfirmModal.vue'

const { logout } = useAuth()
const {
  bucket,
  currentFolderId,
  currentFolderName,
  breadcrumbs,
  files,
  loading,
  error,
  isUploading,
  uploadProgress,
  isCreateFolderOpen,
  isCreatingFolder,
  fileToPreview,
  previewInfo,
  isPreviewOpen,
  previewLoading,
  fileToDelete,
  isDeleteModalOpen,
  isDeleting,
  viewMode,
  initBucket,
  loadFolder,
  navigateToBreadcrumb,
  createFolder,
  uploadFile,
  openPreview,
  closePreview,
  promptDeleteFile,
  cancelDelete,
  executeDeleteFile
} = useDriveBucket()

const showUploadZone = ref(true)
const newFolderNameInput = ref('')

const handleCreateFolder = async () => {
  if (!newFolderNameInput.value.trim()) return
  await createFolder(newFolderNameInput.value)
  newFolderNameInput.value = ''
}

const handleFileUploaded = async (file: File) => {
  await uploadFile(file)
}

onMounted(() => {
  if (!bucket.value) {
    initBucket()
  }
})
</script>

<template>
  <section class="drive-section">
    <!-- Toolbar: Breadcrumbs + Actions -->
    <div class="drive-toolbar glass-panel">
      <!-- Breadcrumbs Path -->
      <DriveBreadcrumb
        :breadcrumbs="breadcrumbs"
        @navigate="navigateToBreadcrumb"
      />

      <!-- Action Buttons -->
      <div class="toolbar-actions">
        <!-- New Folder Trigger -->
        <button
          class="btn-tool"
          :class="{ active: isCreateFolderOpen }"
          title="Crear nueva subcarpeta"
          type="button"
          @click="isCreateFolderOpen = !isCreateFolderOpen"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
            <line x1="12" y1="11" x2="12" y2="17" />
            <line x1="9" y1="14" x2="15" y2="14" />
          </svg>
          Nueva Carpeta
        </button>

        <!-- Toggle Upload Zone -->
        <button
          class="btn-tool"
          :class="{ active: showUploadZone }"
          title="Mostrar/Ocultar zona de subida"
          type="button"
          @click="showUploadZone = !showUploadZone"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
          Subir
        </button>

        <!-- View Mode Switch -->
        <div class="view-switch-group">
          <button
            class="btn-view-switch"
            :class="{ active: viewMode === 'grid' }"
            title="Vista en cuadrícula"
            type="button"
            @click="viewMode = 'grid'"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7" />
              <rect x="14" y="3" width="7" height="7" />
              <rect x="14" y="14" width="7" height="7" />
              <rect x="3" y="14" width="7" height="7" />
            </svg>
          </button>
          <button
            class="btn-view-switch"
            :class="{ active: viewMode === 'list' }"
            title="Vista en lista"
            type="button"
            @click="viewMode = 'list'"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="8" y1="6" x2="21" y2="6" />
              <line x1="8" y1="12" x2="21" y2="12" />
              <line x1="8" y1="18" x2="21" y2="18" />
              <line x1="3" y1="6" x2="3.01" y2="6" />
              <line x1="3" y1="12" x2="3.01" y2="12" />
              <line x1="3" y1="18" x2="3.01" y2="18" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Inline Create Folder Bar -->
    <Transition name="expand">
      <div v-if="isCreateFolderOpen" class="create-folder-bar glass-panel">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="folder-input-icon">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
        </svg>
        <input
          v-model="newFolderNameInput"
          type="text"
          placeholder="Nombre de la nueva carpeta..."
          class="folder-input"
          @keyup.enter="handleCreateFolder"
        />
        <button
          class="btn-create-submit"
          :disabled="isCreatingFolder || !newFolderNameInput.trim()"
          type="button"
          @click="handleCreateFolder"
        >
          {{ isCreatingFolder ? 'Creando...' : 'Crear' }}
        </button>
        <button
          class="btn-create-cancel"
          type="button"
          @click="isCreateFolderOpen = false"
        >
          ✕
        </button>
      </div>
    </Transition>

    <!-- Upload Zone Component -->
    <Transition name="expand">
      <div v-if="showUploadZone" class="upload-zone-wrapper">
        <FileUploadZone
          :uploading="isUploading"
          :progress="uploadProgress"
          @file-selected="handleFileUploaded"
        />
      </div>
    </Transition>

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
        <strong class="error-title">No se pudieron sincronizar los archivos de Google Drive</strong>
        <p class="error-desc">{{ error }}</p>
        <div class="error-actions">
          <button class="btn-error-action" type="button" @click="initBucket">
            🔄 Reintentar
          </button>
          <button class="btn-error-action btn-error-logout" type="button" @click="logout">
            🔑 Volver a iniciar sesión
          </button>
        </div>
      </div>
    </div>

    <!-- Loading Skeleton Grid -->
    <div v-if="loading && files.length === 0" class="drive-grid-skeleton">
      <div v-for="n in 8" :key="n" class="skeleton-file-card glass-panel shimmer" />
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && files.length === 0" class="empty-state glass-panel">
      <div class="empty-icon-circle">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
        </svg>
      </div>
      <h3 class="empty-title">Esta carpeta está vacía</h3>
      <p class="empty-desc">
        Arrastra archivos a la zona de subida superior para almacenarlos en tu Google Drive.
      </p>
    </div>

    <!-- Files Container (Grid or List) -->
    <div
      v-else
      class="files-container"
      :class="viewMode"
    >
      <DriveFileCard
        v-for="file in files"
        :key="file.id"
        :file="file"
        :view-mode="viewMode"
        @click="openPreview(file)"
        @delete="promptDeleteFile(file)"
      />
    </div>

    <!-- Preview Modal -->
    <FilePreviewModal
      :is-open="isPreviewOpen"
      :file="fileToPreview"
      :preview-info="previewInfo"
      :loading="previewLoading"
      @close="closePreview"
    />

    <!-- Delete Confirmation Modal -->
    <DeleteConfirmModal
      :is-open="isDeleteModalOpen"
      title="Eliminar de Google Drive"
      message="¿Estás seguro de que deseas enviar este archivo a la papelera de Google Drive? Esta acción se registrará en la bitácora de auditoría."
      :item-title="fileToDelete?.name"
      :is-deleting="isDeleting"
      @confirm="executeDeleteFile"
      @cancel="cancelDelete"
    />
  </section>
</template>

<style scoped>
.drive-section {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.drive-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  border-radius: 14px;
  flex-wrap: wrap;
  gap: 12px;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-tool {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted);
  font-family: inherit;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-tool:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary);
}

.btn-tool.active {
  background: rgba(0, 255, 198, 0.12);
  border-color: rgba(0, 255, 198, 0.35);
  color: var(--hermes-accent-teal);
}

.view-switch-group {
  display: flex;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 2px;
}

.btn-view-switch {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--hermes-text-muted);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-view-switch:hover {
  color: var(--hermes-text-primary);
}

.btn-view-switch.active {
  background: rgba(255, 255, 255, 0.12);
  color: var(--hermes-accent-blue);
}

/* ── Inline Create Folder ── */
.create-folder-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-radius: 12px;
  border: 1px solid rgba(245, 158, 11, 0.3);
  background: rgba(245, 158, 11, 0.04);
}

.folder-input-icon {
  color: #F59E0B;
  flex-shrink: 0;
}

.folder-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--hermes-text-primary);
  font-family: inherit;
  font-size: 0.88rem;
  outline: none;
}

.folder-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.btn-create-submit {
  padding: 6px 14px;
  border-radius: 8px;
  background: #F59E0B;
  color: #000000;
  font-weight: 700;
  font-size: 0.82rem;
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.btn-create-submit:hover:not(:disabled) {
  transform: scale(1.04);
}

.btn-create-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-create-cancel {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted);
  cursor: pointer;
  font-size: 0.9rem;
}

.upload-zone-wrapper {
  margin-bottom: 4px;
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

/* ── Grid vs List ── */
.files-container.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 14px;
}

.files-container.list {
  display: flex;
  flex-direction: column;
  gap: 8px;
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

/* Skeleton */
.drive-grid-skeleton {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 14px;
}

.skeleton-file-card {
  height: 160px;
  border-radius: 12px;
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

.expand-enter-active,
.expand-leave-active {
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  max-height: 200px;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-8px);
}
</style>

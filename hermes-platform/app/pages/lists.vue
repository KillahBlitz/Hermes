<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useLists, type WishlistItem, type TodoSection as ITodoSection, type TodoTask } from '~/composables/useLists'
import { useAuth } from '~/composables/useAuth'
import WishlistSection from '~/components/organisms/WishlistSection.vue'
import TodoSection from '~/components/organisms/TodoSection.vue'
import WishlistModal from '~/components/organisms/WishlistModal.vue'
import WishlistPhotoUploadModal from '~/components/organisms/WishlistPhotoUploadModal.vue'
import TodoSectionModal from '~/components/organisms/TodoSectionModal.vue'
import TodoTaskModal from '~/components/organisms/TodoTaskModal.vue'
import DeleteConfirmModal from '~/components/organisms/DeleteConfirmModal.vue'

useHead({
  title: 'Listas & Deseos | Hermes',
  meta: [{ name: 'description', content: 'Lista de deseos con fotos en Google Drive y tareas To-Do estilo Microsoft.' }]
})

const { isAuthenticated } = useAuth()
const lists = useLists()

// Modales de Wishlist
const showWishlistModal = ref(false)
const wishlistItemToEdit = ref<WishlistItem | null>(null)
const showPhotoUploadModal = ref(false)
const photoUploadItem = ref<WishlistItem | null>(null)

// Modales de To-Do
const showSectionModal = ref(false)
const sectionToEdit = ref<ITodoSection | null>(null)
const showTaskModal = ref(false)
const taskToEdit = ref<TodoTask | null>(null)

// Modal de eliminación
const showDeleteModal = ref(false)
const deleteTargetType = ref<'wishlist' | 'section' | 'task'>('wishlist')
const deleteTargetItem = ref<any>(null)
const deleteTargetTitle = ref('')
const isDeleting = ref(false)

// Toast / Notification
const toastMessage = ref<string | null>(null)
const toastType = ref<'success' | 'error'>('success')

const showToast = (msg: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = null
  }, 4000)
}

onMounted(async () => {
  await lists.setToolTab('wishlist')
})

// ─────────────────────────────────────────────────────────────
// ACCIONES WISHLIST
// ─────────────────────────────────────────────────────────────

const openCreateWishlist = () => {
  wishlistItemToEdit.value = null
  showWishlistModal.value = true
}

const openEditWishlist = (item: WishlistItem) => {
  wishlistItemToEdit.value = item
  showWishlistModal.value = true
}

const openUploadPhoto = (item: WishlistItem) => {
  photoUploadItem.value = item
  showPhotoUploadModal.value = true
}

const handleSaveWishlist = async (payload: any) => {
  try {
    if (payload.id) {
      await lists.updateWishlistItem(payload.id, payload)
      showToast('Deseo actualizado exitosamente.')
    } else {
      await lists.createWishlistItem(payload)
      showToast('Deseo creado exitosamente.')
    }
    showWishlistModal.value = false
  } catch (err: any) {
    showToast(err.message || 'Error al guardar deseo', 'error')
  }
}

const handleToggleWishlistStatus = async (item: WishlistItem) => {
  try {
    const nextStatus = item.status === 'PURCHASED' ? 'PENDING' : 'PURCHASED'
    await lists.updateWishlistStatus(item.id, nextStatus)
    showToast(nextStatus === 'PURCHASED' ? '¡Felicidades! Deseo marcado como comprado 🎉' : 'Deseo marcado como pendiente.')
  } catch (err: any) {
    showToast(err.message || 'Error al cambiar estado', 'error')
  }
}

const isUploadingPhoto = ref(false)

const handleUploadPhoto = async (file: File) => {
  if (!photoUploadItem.value) return
  isUploadingPhoto.value = true
  try {
    const updated = await lists.uploadWishlistPhoto(photoUploadItem.value.id, file)
    photoUploadItem.value = updated
    showToast('Foto guardada en Google Drive (hermes/whitelist) exitosamente 📸')
  } catch (err: any) {
    showToast(err.message || 'Error al subir foto a Google Drive', 'error')
  } finally {
    isUploadingPhoto.value = false
  }
}

const promptDeleteWishlist = (item: WishlistItem) => {
  deleteTargetType.value = 'wishlist'
  deleteTargetItem.value = item
  deleteTargetTitle.value = item.name
  showDeleteModal.value = true
}

// ─────────────────────────────────────────────────────────────
// ACCIONES TO-DO
// ─────────────────────────────────────────────────────────────

const openCreateSection = () => {
  sectionToEdit.value = null
  showSectionModal.value = true
}

const openEditSection = (sec: ITodoSection) => {
  sectionToEdit.value = sec
  showSectionModal.value = true
}

const handleSaveSection = async (payload: any) => {
  try {
    if (payload.id) {
      await lists.updateTodoSection(payload.id, payload)
      showToast('Sección actualizada.')
    } else {
      await lists.createTodoSection(payload)
      showToast('Sección creada exitosamente.')
    }
    showSectionModal.value = false
  } catch (err: any) {
    showToast(err.message || 'Error al guardar sección', 'error')
  }
}

const promptDeleteSection = (sec: ITodoSection) => {
  deleteTargetType.value = 'section'
  deleteTargetItem.value = sec
  deleteTargetTitle.value = `Sección "${sec.name}"`
  showDeleteModal.value = true
}

const handleQuickCreateTask = async (payload: { title: string; section_id?: string }) => {
  try {
    await lists.createTodoTask(payload)
  } catch (err: any) {
    showToast(err.message || 'Error al crear tarea rápida', 'error')
  }
}

const openEditTask = (task: TodoTask) => {
  taskToEdit.value = task
  showTaskModal.value = true
}

const handleSaveTask = async (payload: any) => {
  try {
    if (payload.id) {
      await lists.updateTodoTask(payload.id, payload)
      showToast('Tarea actualizada.')
    } else {
      await lists.createTodoTask(payload)
      showToast('Tarea creada exitosamente.')
    }
    showTaskModal.value = false
  } catch (err: any) {
    showToast(err.message || 'Error al guardar tarea', 'error')
  }
}

const handleToggleTask = async (task: TodoTask) => {
  try {
    await lists.toggleTodoTask(task.id, !task.is_completed)
  } catch (err: any) {
    showToast(err.message || 'Error al cambiar estado de la tarea', 'error')
  }
}

const promptDeleteTask = (task: TodoTask) => {
  deleteTargetType.value = 'task'
  deleteTargetItem.value = task
  deleteTargetTitle.value = task.title
  showDeleteModal.value = true
}

// ─────────────────────────────────────────────────────────────
// ELIMINACIÓN GENERAL
// ─────────────────────────────────────────────────────────────

const executeDelete = async () => {
  if (!deleteTargetItem.value) return
  isDeleting.value = true
  try {
    if (deleteTargetType.value === 'wishlist') {
      await lists.deleteWishlistItem(deleteTargetItem.value.id)
      showToast('Deseo eliminado.')
    } else if (deleteTargetType.value === 'section') {
      await lists.deleteTodoSection(deleteTargetItem.value.id)
      showToast('Sección eliminada.')
    } else if (deleteTargetType.value === 'task') {
      await lists.deleteTodoTask(deleteTargetItem.value.id)
      showToast('Tarea eliminada.')
    }
    showDeleteModal.value = false
  } catch (err: any) {
    showToast(err.message || 'Error al eliminar', 'error')
  } finally {
    isDeleting.value = false
  }
}
</script>

<template>
  <div class="lists-page-container">
    <!-- Header Principal -->
    <div class="page-top-bar">
      <div class="title-group">
        <h1 class="page-title">
          <span class="title-icon text-accent-pink">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
            </svg>
          </span>
          Listas & Deseos
        </h1>
        <p class="page-desc">
          Catálogo de compras futuras con almacenamiento de fotos en Google Drive y tareas rutinarias estilo Microsoft To-Do.
        </p>
      </div>

      <!-- Selector de Herramienta Superior -->
      <div class="tool-tabs-switch glass-panel">
        <button
          type="button"
          class="tool-tab-btn"
          :class="{ active: lists.activeToolTab.value === 'wishlist' }"
          @click="lists.setToolTab('wishlist')"
        >
          <span class="tab-emoji">🎁</span>
          <span>Lista de Deseos</span>
        </button>

        <button
          type="button"
          class="tool-tab-btn"
          :class="{ active: lists.activeToolTab.value === 'todo' }"
          @click="lists.setToolTab('todo')"
        >
          <span class="tab-emoji">☑️</span>
          <span>Tareas (To-Do)</span>
        </button>
      </div>
    </div>

    <!-- Alerta / Notificación Toast -->
    <div v-if="toastMessage" class="toast-popup" :class="toastType">
      <span>{{ toastMessage }}</span>
    </div>

    <!-- Vista 1: Lista de Deseos (Wishlist) -->
    <div v-if="lists.activeToolTab.value === 'wishlist'" class="view-content">
      <WishlistSection
        :items="lists.wishlistItems.value"
        :stats="lists.wishlistStats.value"
        :filter-status="lists.wishlistFilterStatus.value"
        :filter-category="lists.wishlistFilterCategory.value"
        :filter-priority="lists.wishlistFilterPriority.value"
        :search-query="lists.wishlistSearch.value"
        :loading="lists.loading.value"
        @update-filters="(s, c, p, q) => {
          lists.wishlistFilterStatus.value = s
          lists.wishlistFilterCategory.value = c
          lists.wishlistFilterPriority.value = p
          lists.wishlistSearch.value = q
          lists.fetchWishlist()
        }"
        @toggle-status="handleToggleWishlistStatus"
        @edit-item="openEditWishlist"
        @upload-photo="openUploadPhoto"
        @delete-item="promptDeleteWishlist"
        @new-item="openCreateWishlist"
      />
    </div>

    <!-- Vista 2: Lista de Tareas (Microsoft To-Do) -->
    <div v-else-if="lists.activeToolTab.value === 'todo'" class="view-content">
      <TodoSection
        :sections="lists.todoSections.value"
        :tasks="lists.todoTasks.value"
        :selected-section-id="lists.selectedSectionId.value"
        :search-query="lists.todoSearch.value"
        :loading="lists.loading.value"
        @select-section="lists.selectSection"
        @update-search="(q) => {
          lists.todoSearch.value = q
          lists.fetchTodoTasks()
        }"
        @create-quick-task="handleQuickCreateTask"
        @toggle-task="handleToggleTask"
        @edit-task="openEditTask"
        @delete-task="promptDeleteTask"
        @new-section="openCreateSection"
        @edit-section="openEditSection"
        @delete-section="promptDeleteSection"
      />
    </div>

    <!-- MODALES -->
    <WishlistModal
      :show="showWishlistModal"
      :item-to-edit="wishlistItemToEdit"
      @close="showWishlistModal = false"
      @save="handleSaveWishlist"
    />

    <WishlistPhotoUploadModal
      :show="showPhotoUploadModal"
      :item="photoUploadItem"
      :loading="isUploadingPhoto"
      @close="showPhotoUploadModal = false"
      @upload="handleUploadPhoto"
    />

    <TodoSectionModal
      :show="showSectionModal"
      :section-to-edit="sectionToEdit"
      @close="showSectionModal = false"
      @save="handleSaveSection"
    />

    <TodoTaskModal
      :show="showTaskModal"
      :sections="lists.todoSections.value"
      :task-to-edit="taskToEdit"
      :default-section-id="lists.selectedSectionId.value"
      @close="showTaskModal = false"
      @save="handleSaveTask"
    />

    <DeleteConfirmModal
      :is-open="showDeleteModal"
      title="Eliminar elemento"
      message="¿Estás seguro de que deseas eliminar este elemento permanentemente?"
      :item-title="deleteTargetTitle"
      :is-deleting="isDeleting"
      @confirm="executeDelete"
      @cancel="showDeleteModal = false"
    />
  </div>
</template>

<style scoped>
.lists-page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding-bottom: 60px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
}

.title-icon {
  display: flex;
  align-items: center;
}

.page-desc {
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.88rem;
  margin: 0;
  max-width: 580px;
}

/* Tool Tab Switcher */
.tool-tabs-switch {
  display: flex;
  padding: 4px;
  background: rgba(23, 23, 28, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  gap: 4px;
}

.tool-tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 8px 16px;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.86rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.tool-tab-btn:hover {
  color: var(--hermes-text-primary, #F4F4F5);
}

.tool-tab-btn.active {
  background: rgba(0, 229, 255, 0.12);
  border-color: rgba(0, 229, 255, 0.3);
  color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 16px rgba(0, 229, 255, 0.15);
}

.tab-emoji {
  font-size: 1rem;
}

/* Toast */
.toast-popup {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 20px;
  border-radius: 12px;
  background: rgba(23, 23, 28, 0.95);
  border: 1px solid rgba(0, 255, 198, 0.4);
  color: var(--hermes-accent-teal, #00FFC6);
  font-size: 0.86rem;
  font-weight: 700;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  z-index: 200;
  animation: slideUp 0.2s ease-out;
}

.toast-popup.error {
  border-color: rgba(255, 0, 127, 0.4);
  color: var(--hermes-accent-pink, #FF007F);
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@media (max-width: 768px) {
  .page-top-bar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>

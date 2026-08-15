<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useProgress } from '~/composables/useProgress'
import type { Roadmap, RoadmapNode, Milestone, ZettelNote } from '~/composables/useProgress'
import RoadmapCanvasView from '~/components/organisms/RoadmapCanvasView.vue'
import MilestonesTrackerView from '~/components/organisms/MilestonesTrackerView.vue'
import ZettelkastenVaultView from '~/components/organisms/ZettelkastenVaultView.vue'
import RoadmapModal from '~/components/organisms/RoadmapModal.vue'
import RoadmapNodeModal from '~/components/organisms/RoadmapNodeModal.vue'
import MilestoneModal from '~/components/organisms/MilestoneModal.vue'
import MarkdownNoteModal from '~/components/organisms/MarkdownNoteModal.vue'

useHead({
  title: 'Progreso | Hermes',
  meta: [{ name: 'description', content: 'Árbol de mapas, gestor de hitos de proyectos a gran escala y bóveda de conocimiento Zettelkasten.' }]
})

const progress = useProgress()

// Toast Feedback
const toastMessage = ref('')
const toastType = ref<'success' | 'error'>('success')
const toastVisible = ref(false)

const showToast = (msg: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = msg
  toastType.value = type
  toastVisible.value = true
  setTimeout(() => {
    toastVisible.value = false
  }, 3500)
}

// ─────────────────────────────────────────────────────────────
// MODALES ESTADOS
// ─────────────────────────────────────────────────────────────

// Roadmap Modals
const showRoadmapModal = ref(false)
const roadmapToEdit = ref<Roadmap | null>(null)

const showNodeModal = ref(false)
const nodeToEdit = ref<RoadmapNode | null>(null)
const targetRoadmapForNode = ref<Roadmap | null>(null)

// Milestone Modals
const showMilestoneModal = ref(false)
const milestoneToEdit = ref<Milestone | null>(null)

// Note Modal (para nodos de roadmap o vista rápida)
const showNoteModal = ref(false)
const noteForModal = ref<ZettelNote | null>(null)

// Delete Confirm Modal
const showDeleteConfirmModal = ref(false)
const deleteAction = ref<(() => Promise<void>) | null>(null)
const deleteTargetTitle = ref('')

// ─────────────────────────────────────────────────────────────
// ACCIONES ROADMAPS
// ─────────────────────────────────────────────────────────────

const openCreateRoadmap = () => {
  roadmapToEdit.value = null
  showRoadmapModal.value = true
}

const openEditRoadmap = (r: Roadmap) => {
  roadmapToEdit.value = r
  showRoadmapModal.value = true
}

const handleSaveRoadmap = async (data: { title: string; description?: string; category: string; color: string }) => {
  try {
    if (roadmapToEdit.value) {
      await progress.updateRoadmap(roadmapToEdit.value.id, data)
      showToast('Árbol de mapas actualizado exitosamente 🗺️')
    } else {
      await progress.createRoadmap(data)
      showToast('Nueva ruta de aprendizaje creada exitosamente 🚀')
    }
    showRoadmapModal.value = false
  } catch (err: any) {
    showToast(err.message || 'Error al guardar el roadmap', 'error')
  }
}

const promptDeleteRoadmap = (r: Roadmap) => {
  deleteTargetTitle.value = `el árbol de mapas "${r.title}"`
  deleteAction.value = async () => {
    await progress.deleteRoadmap(r.id)
    showToast('Árbol de mapas eliminado')
  }
  showDeleteConfirmModal.value = true
}

const openCreateNode = (roadmap: Roadmap) => {
  targetRoadmapForNode.value = roadmap
  nodeToEdit.value = null
  showNodeModal.value = true
}

const openEditNode = (roadmap: Roadmap, node: RoadmapNode) => {
  targetRoadmapForNode.value = roadmap
  nodeToEdit.value = node
  showNodeModal.value = true
}

const handleSaveNode = async (nodeData: {
  id?: string
  title: string
  icon: string
  color: string
  status: 'PENDIENTE' | 'EN_CURSO' | 'DOMINADO'
  description?: string
}) => {
  if (!targetRoadmapForNode.value) return
  try {
    const r = targetRoadmapForNode.value
    if (nodeData.id) {
      // Editar nodo existente
      const idx = r.nodes.findIndex(n => n.id === nodeData.id)
      if (idx !== -1 && r.nodes[idx]) {
        r.nodes[idx] = {
          ...r.nodes[idx],
          title: nodeData.title,
          icon: nodeData.icon,
          color: nodeData.color,
          status: nodeData.status,
          description: nodeData.description
        }
      }
    } else {
      // Crear nuevo nodo con posición escalonada
      const newX = 100 + (r.nodes.length % 4) * 280
      const newY = 100 + Math.floor(r.nodes.length / 4) * 160
      r.nodes.push({
        id: `node_${Date.now()}`,
        title: nodeData.title,
        icon: nodeData.icon,
        color: nodeData.color,
        status: nodeData.status,
        description: nodeData.description,
        x: newX,
        y: newY
      })
    }

    await progress.updateRoadmap(r.id, { nodes: r.nodes })
    showToast('Módulo del roadmap guardado ⚡')
    showNodeModal.value = false
  } catch (err: any) {
    showToast(err.message || 'Error al guardar el módulo', 'error')
  }
}

const promptDeleteNode = (roadmap: Roadmap, node: RoadmapNode) => {
  deleteTargetTitle.value = `el módulo "${node.title}"`
  deleteAction.value = async () => {
    roadmap.nodes = roadmap.nodes.filter(n => n.id !== node.id)
    roadmap.edges = roadmap.edges.filter(e => e.source_node_id !== node.id && e.target_node_id !== node.id)
    await progress.updateRoadmap(roadmap.id, { nodes: roadmap.nodes, edges: roadmap.edges })
    showToast('Módulo eliminado del roadmap')
  }
  showDeleteConfirmModal.value = true
}

const handleUpdateRoadmapData = async (roadmap: Roadmap) => {
  try {
    await progress.updateRoadmap(roadmap.id, {
      nodes: roadmap.nodes,
      edges: roadmap.edges
    })
  } catch (err: any) {
    console.error('Error al sincronizar posiciones:', err)
  }
}

// ─────────────────────────────────────────────────────────────
// ACCIONES MARKDOWN & APUNTES
// ─────────────────────────────────────────────────────────────

const handleOpenNodeNote = async (node: RoadmapNode) => {
  try {
    // Si el nodo ya tiene una nota vinculada, buscarla
    let targetNote = null
    if (node.note_id) {
      targetNote = await progress.fetchNote(node.note_id)
    }
    if (!targetNote) {
      targetNote = await progress.fetchNote(node.title)
    }

    if (!targetNote) {
      // Crear borrador inicial para este nodo
      targetNote = await progress.createNote({
        title: node.title,
        content_md: `# ${node.title}\n\nBitácora y apuntes técnicos de este módulo del roadmap.\n\n- Estado: **${node.status}**\n- Descripción: ${node.description || 'Sin descripción'}\n\n#${node.status.toLowerCase()}\n`,
        roadmap_node_id: node.id
      })
      node.note_id = targetNote.id
      node.note_title = targetNote.title
      if (progress.activeRoadmap.value) {
        await progress.updateRoadmap(progress.activeRoadmap.value.id, { nodes: progress.activeRoadmap.value.nodes })
      }
    }

    noteForModal.value = targetNote
    showNoteModal.value = true
  } catch (err: any) {
    showToast(err.message || 'Error al abrir los apuntes .md', 'error')
  }
}

const handleSaveModalNote = async (noteData: {
  id?: string
  title: string
  content_md: string
  tags?: string[]
  roadmap_node_id?: string
}) => {
  try {
    if (noteData.id) {
      await progress.updateNote(noteData.id, noteData)
      showToast('Apuntes .md guardados exitosamente 📝')
    } else {
      await progress.createNote(noteData as any)
      showToast('Nueva nota creada exitosamente 📝')
    }
    showNoteModal.value = false
  } catch (err: any) {
    showToast(err.message || 'Error al guardar la nota', 'error')
  }
}

// ─────────────────────────────────────────────────────────────
// ACCIONES HITOS (MILESTONES)
// ─────────────────────────────────────────────────────────────

const openCreateMilestone = () => {
  milestoneToEdit.value = null
  showMilestoneModal.value = true
}

const openEditMilestone = (m: Milestone) => {
  milestoneToEdit.value = m
  showMilestoneModal.value = true
}

const handleSaveMilestone = async (data: any) => {
  try {
    if (milestoneToEdit.value) {
      await progress.updateMilestone(milestoneToEdit.value.id, data)
      showToast('Hito estratégico actualizado 🎯')
    } else {
      await progress.createMilestone(data)
      showToast('Nuevo hito registrado exitosamente 🎯')
    }
    showMilestoneModal.value = false
  } catch (err: any) {
    showToast(err.message || 'Error al guardar el hito', 'error')
  }
}

const promptDeleteMilestone = (m: Milestone) => {
  deleteTargetTitle.value = `el hito "${m.title}"`
  deleteAction.value = async () => {
    await progress.deleteMilestone(m.id)
    showToast('Hito eliminado')
  }
  showDeleteConfirmModal.value = true
}

const handleToggleMilestoneTopic = async (mId: string, tId: string, comp: boolean) => {
  try {
    await progress.toggleMilestoneTopic(mId, tId, comp)
  } catch (err: any) {
    showToast(err.message || 'Error al cambiar tema', 'error')
  }
}

// ─────────────────────────────────────────────────────────────
// ACCIONES ZETTELKASTEN
// ─────────────────────────────────────────────────────────────

const handleSaveVaultNote = async (note: ZettelNote) => {
  try {
    await progress.updateNote(note.id, note)
    showToast('Nota Zettelkasten actualizada 🧠')
  } catch (err: any) {
    showToast(err.message || 'Error al guardar la nota', 'error')
  }
}

const handleCreateVaultNote = async () => {
  try {
    const title = `Nueva Nota ${progress.notes.value.length + 1}`
    const created = await progress.createNote({
      title,
      content_md: `# ${title}\n\nEscribe aquí tus ideas y usa [[Wikilinks]] para entrelazar con otras notas.\n\n#ideas\n`
    })
    showToast('Nota creada 📝')
  } catch (err: any) {
    showToast(err.message || 'Error al crear la nota', 'error')
  }
}

const promptDeleteVaultNote = (note: ZettelNote) => {
  deleteTargetTitle.value = `la nota "${note.title}"`
  deleteAction.value = async () => {
    await progress.deleteNote(note.id)
    showToast('Nota eliminada de la bóveda')
  }
  showDeleteConfirmModal.value = true
}

const executeDelete = async () => {
  if (deleteAction.value) {
    try {
      await deleteAction.value()
    } catch (err: any) {
      showToast(err.message || 'Error al eliminar', 'error')
    }
  }
  showDeleteConfirmModal.value = false
  deleteAction.value = null
}

onMounted(async () => {
  await progress.fetchRoadmaps()
})
</script>

<template>
  <div class="progress-module-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-main">
        <h1 class="page-title">
          <span class="title-icon text-accent-blue">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" />
              <path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" />
              <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0" />
              <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5" />
            </svg>
          </span>
          Progreso & Conocimiento
        </h1>
        <p class="page-desc">
          Rutas de aprendizaje modulares, monitoreo de hitos y proyectos a gran escala, y bóveda Zettelkasten interconectada.
        </p>
      </div>

      <!-- 3 Tools Selector Pills -->
      <div class="tool-tabs-container">
        <button
          type="button"
          class="tool-tab-btn"
          :class="{ 'is-active': progress.activeToolTab.value === 'roadmaps' }"
          @click="progress.setToolTab('roadmaps')"
        >
          <span class="tab-icon">🗺️</span>
          <span class="tab-label">Árbol de Mapas</span>
        </button>

        <button
          type="button"
          class="tool-tab-btn"
          :class="{ 'is-active': progress.activeToolTab.value === 'milestones' }"
          @click="progress.setToolTab('milestones')"
        >
          <span class="tab-icon">🎯</span>
          <span class="tab-label">Gestor de Hitos</span>
        </button>

        <button
          type="button"
          class="tool-tab-btn"
          :class="{ 'is-active': progress.activeToolTab.value === 'zettelkasten' }"
          @click="progress.setToolTab('zettelkasten')"
        >
          <span class="tab-icon">🧠</span>
          <span class="tab-label">Red Zettelkasten</span>
        </button>
      </div>
    </div>

    <!-- Active Tool Content View -->
    <div class="tool-view-wrapper">
      <!-- 1. ÁRBOL DE MAPAS -->
      <RoadmapCanvasView
        v-if="progress.activeToolTab.value === 'roadmaps'"
        :roadmaps="progress.roadmaps.value"
        :active-roadmap="progress.activeRoadmap.value"
        :loading="progress.loading.value"
        @select-roadmap="progress.activeRoadmapId.value = $event"
        @create-roadmap="openCreateRoadmap"
        @edit-roadmap="openEditRoadmap"
        @delete-roadmap="promptDeleteRoadmap"
        @create-node="openCreateNode"
        @edit-node="openEditNode"
        @delete-node="promptDeleteNode"
        @open-note="handleOpenNodeNote"
        @update-roadmap-data="handleUpdateRoadmapData"
      />

      <!-- 2. GESTOR DE HITOS -->
      <MilestonesTrackerView
        v-else-if="progress.activeToolTab.value === 'milestones'"
        :milestones="progress.milestones.value"
        :selected-category="progress.milestonesFilterCategory.value"
        :selected-status="progress.milestonesFilterStatus.value"
        :loading="progress.loading.value"
        @update:category="progress.milestonesFilterCategory.value = $event; progress.fetchMilestones()"
        @update:status="progress.milestonesFilterStatus.value = $event; progress.fetchMilestones()"
        @create="openCreateMilestone"
        @edit="openEditMilestone"
        @delete="promptDeleteMilestone"
        @toggle-topic="handleToggleMilestoneTopic"
      />

      <!-- 3. RED ZETTELKASTEN -->
      <ZettelkastenVaultView
        v-else-if="progress.activeToolTab.value === 'zettelkasten'"
        :notes="progress.notes.value"
        :active-note="progress.activeNote.value"
        :search="progress.notesSearch.value"
        :selected-tag="progress.selectedTag.value"
        :is-graph-view="progress.isGraphView.value"
        :graph-data="progress.graphData.value"
        :loading="progress.loading.value"
        @update:search="progress.notesSearch.value = $event; progress.fetchNotes()"
        @update:selected-tag="progress.selectedTag.value = $event; progress.fetchNotes()"
        @update:is-graph-view="progress.isGraphView.value = $event"
        @select-note="progress.activeNote.value = $event"
        @create-note="handleCreateVaultNote"
        @save-note="handleSaveVaultNote"
        @delete-note="promptDeleteVaultNote"
        @open-wikilink="progress.openWikilink"
      />
    </div>

    <!-- MODALES -->
    <RoadmapModal
      :show="showRoadmapModal"
      :roadmap-to-edit="roadmapToEdit"
      @close="showRoadmapModal = false"
      @save="handleSaveRoadmap"
    />

    <RoadmapNodeModal
      :show="showNodeModal"
      :node-to-edit="nodeToEdit"
      @close="showNodeModal = false"
      @save="handleSaveNode"
    />

    <MilestoneModal
      :show="showMilestoneModal"
      :milestone-to-edit="milestoneToEdit"
      @close="showMilestoneModal = false"
      @save="handleSaveMilestone"
    />

    <MarkdownNoteModal
      :show="showNoteModal"
      :note="noteForModal"
      @close="showNoteModal = false"
      @save="handleSaveModalNote"
      @open-wikilink="progress.openWikilink"
    />

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirmModal" class="modal-backdrop" @click.self="showDeleteConfirmModal = false">
      <div class="modal-card glass-panel delete-modal">
        <h3 class="delete-title">¿Confirmas la eliminación?</h3>
        <p class="delete-desc">Estás a punto de eliminar <strong>{{ deleteTargetTitle }}</strong>. Esta acción no se puede deshacer.</p>
        <div class="delete-actions">
          <button type="button" class="btn-cancel" @click="showDeleteConfirmModal = false">Cancelar</button>
          <button type="button" class="btn-delete" @click="executeDelete">Sí, Eliminar</button>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <Transition name="toast">
      <div v-if="toastVisible" class="toast-notification" :class="`toast-${toastType}`">
        {{ toastMessage }}
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.progress-module-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  flex-wrap: wrap;
}

.header-main {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
  font-size: 1.7rem;
  font-weight: 800;
  color: var(--hermes-text-primary);
}

.title-icon {
  display: flex;
}

.text-accent-blue {
  color: var(--hermes-accent-blue, #00E5FF);
}

.page-desc {
  margin: 0;
  font-size: 0.9rem;
  color: var(--hermes-text-muted);
  max-width: 580px;
  line-height: 1.4;
}

.tool-tabs-container {
  display: flex;
  background: rgba(23, 23, 28, 0.9);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.tool-tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--hermes-text-muted);
  font-size: 0.84rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: inherit;
}

.tool-tab-btn:hover {
  color: var(--hermes-text-primary);
}

.tool-tab-btn.is-active {
  background: rgba(0, 229, 255, 0.18);
  color: var(--hermes-accent-blue, #00E5FF);
  border: 1px solid rgba(0, 229, 255, 0.35);
  box-shadow: 0 0 14px rgba(0, 229, 255, 0.25);
}

.tool-view-wrapper {
  display: flex;
  flex-direction: column;
}

/* Modales y Delete Prompt */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.delete-modal {
  width: 100%;
  max-width: 420px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 77, 77, 0.3);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.delete-title {
  margin: 0;
  font-size: 1.15rem;
  color: var(--hermes-text-primary);
}

.delete-desc {
  margin: 0;
  font-size: 0.85rem;
  color: var(--hermes-text-muted);
  line-height: 1.4;
}

.delete-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.btn-cancel {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted);
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-delete {
  padding: 8px 16px;
  background: rgba(255, 77, 77, 0.2);
  border: 1px solid rgba(255, 77, 77, 0.5);
  color: #ff4d4d;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
}

.btn-delete:hover {
  background: rgba(255, 77, 77, 0.35);
}

/* Toast */
.toast-notification {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1200;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 0.88rem;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.toast-success {
  background: rgba(0, 255, 198, 0.15);
  border: 1px solid var(--hermes-accent-teal, #00FFC6);
  color: var(--hermes-accent-teal, #00FFC6);
}

.toast-error {
  background: rgba(255, 77, 77, 0.15);
  border: 1px solid #ff4d4d;
  color: #ff4d4d;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(16px);
}
</style>

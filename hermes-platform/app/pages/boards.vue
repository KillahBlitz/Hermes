<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { useBoards } from '~/composables/useBoards'
import type { Habit, Task } from '~/composables/useBoards'
import KanbanBoardView from '~/components/organisms/KanbanBoardView.vue'
import BacklogListView from '~/components/organisms/BacklogListView.vue'
import ArchivedDoneView from '~/components/organisms/ArchivedDoneView.vue'
import HabitsBoardView from '~/components/organisms/HabitsBoardView.vue'
import StickyNotesCanvas from '~/components/organisms/StickyNotesCanvas.vue'
import TaskModal from '~/components/organisms/TaskModal.vue'
import EpicManagerModal from '~/components/organisms/EpicManagerModal.vue'
import HabitModal from '~/components/organisms/HabitModal.vue'

useHead({
  title: 'Tableros Inteligentes | Hermes',
  meta: [
    {
      name: 'description',
      content: 'Tableros Kanban de actividades, seguimiento de hábitos de 21 días y pizarrón de ideas con post-its.'
    }
  ]
})

const { isAuthenticated } = useAuth()
const boards = useBoards()

// Modales
const showTaskModal = ref(false)
const taskToEdit = ref<Task | null>(null)
const defaultTaskStatus = ref('TODO')

const showEpicModal = ref(false)

const showHabitModal = ref(false)
const habitToEdit = ref<Habit | null>(null)

const modalLoading = ref(false)

onMounted(async () => {
  if (isAuthenticated.value) {
    await boards.refreshAll()
  }
})

// ─────────────────────────────────────────────────────────────
// ACCIONES DE TAREAS & KANBAN
// ─────────────────────────────────────────────────────────────

const handleOpenNewTask = (statusDefault: string = 'TODO') => {
  taskToEdit.value = null
  defaultTaskStatus.value = statusDefault
  showTaskModal.value = true
}

const handleOpenEditTask = (task: Task) => {
  taskToEdit.value = task
  showTaskModal.value = true
}

const handleSaveTask = async (payload: any) => {
  modalLoading.value = true
  try {
    if (payload.id) {
      await boards.updateTask(payload.id, payload)
    } else {
      await boards.createTask(payload)
    }
    showTaskModal.value = false
  } catch (err: any) {
    alert(err.message || 'Error al guardar la tarea')
  } finally {
    modalLoading.value = false
  }
}

const handleDeleteTask = async (task: Task) => {
  if (confirm(`¿Estás seguro de eliminar permanentemente la tarea "${task.title}"?`)) {
    try {
      await boards.deleteTask(task.id)
    } catch (err: any) {
      alert(err.message || 'Error al eliminar la tarea')
    }
  }
}

const handleMoveTaskStatus = async (taskId: string, newStatus: 'TODO' | 'IN_PROGRESS' | 'TESTING' | 'DONE') => {
  try {
    await boards.updateTaskStatus(taskId, newStatus)
  } catch (err: any) {
    alert(err.message || 'Error al mover de columna')
  }
}

const handleMoveToBacklog = async (task: Task) => {
  try {
    await boards.updateTaskLocation(task.id, 'BACKLOG')
  } catch (err: any) {
    alert(err.message || 'Error al mover al Backlog')
  }
}

const handleMoveToBoard = async (task: Task) => {
  try {
    await boards.updateTaskLocation(task.id, 'BOARD')
  } catch (err: any) {
    alert(err.message || 'Error al pasar al Tablero')
  }
}

// ─────────────────────────────────────────────────────────────
// ACCIONES DE ÉPICAS
// ─────────────────────────────────────────────────────────────

const handleCreateEpic = async (payload: { name: string; description?: string; color: string; icon: string }) => {
  modalLoading.value = true
  try {
    await boards.createEpic(payload)
  } catch (err: any) {
    alert(err.message || 'Error al crear la épica')
  } finally {
    modalLoading.value = false
  }
}

const handleDeleteEpic = async (epicId: string) => {
  if (confirm('¿Eliminar esta épica? Las tareas asociadas quedarán sin épica asignada.')) {
    try {
      await boards.deleteEpic(epicId)
    } catch (err: any) {
      alert(err.message || 'Error al eliminar la épica')
    }
  }
}

// ─────────────────────────────────────────────────────────────
// ACCIONES DE HÁBITOS
// ─────────────────────────────────────────────────────────────

const handleOpenNewHabit = () => {
  habitToEdit.value = null
  showHabitModal.value = true
}

const handleOpenEditHabit = (habit: Habit) => {
  habitToEdit.value = habit
  showHabitModal.value = true
}

const handleSaveHabit = async (payload: any) => {
  modalLoading.value = true
  try {
    if (payload.id) {
      await boards.updateHabit(payload.id, payload)
    } else {
      await boards.createHabit(payload)
    }
    showHabitModal.value = false
  } catch (err: any) {
    alert(err.message || 'Error al guardar el hábito')
  } finally {
    modalLoading.value = false
  }
}

const handleDeleteHabit = async (habit: Habit) => {
  if (confirm(`¿Eliminar el hábito "${habit.title}" y su progreso de 21 días?`)) {
    try {
      await boards.deleteHabit(habit.id)
    } catch (err: any) {
      alert(err.message || 'Error al eliminar el hábito')
    }
  }
}

const handleCheckHabitDay = async (habitId: string, dayNumber: number, newStatus: 'COMPLETED' | 'FAILED' | 'PENDING') => {
  try {
    await boards.checkHabitDay(habitId, dayNumber, newStatus)
  } catch (err: any) {
    console.error('Error al registrar día:', err)
  }
}

// ─────────────────────────────────────────────────────────────
// ACCIONES DE POST-ITS
// ─────────────────────────────────────────────────────────────

const handleCreateNote = async (payload: { title?: string; content: string; color: string; x: number; y: number }) => {
  try {
    await boards.createNote(payload)
  } catch (err: any) {
    alert(err.message || 'Error al crear la nota')
  }
}

const handleUpdateNote = async (id: string, payload: any) => {
  try {
    await boards.updateNote(id, payload)
  } catch (err: any) {
    console.error('Error al actualizar nota:', err)
  }
}

const handleUpdateNotePosition = async (id: string, x: number, y: number, zIndex?: number) => {
  await boards.updateNotePosition(id, x, y, zIndex)
}

const handleDeleteNote = async (id: string) => {
  try {
    await boards.deleteNote(id)
  } catch (err: any) {
    alert(err.message || 'Error al eliminar la nota')
  }
}
</script>

<template>
  <div class="boards-page-container">
    <!-- Header Principal -->
    <header class="boards-header">
      <div class="title-meta-group">
        <h1 class="page-title">
          <span class="title-icon text-accent-blue">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="9" rx="1" />
              <rect x="14" y="3" width="7" height="5" rx="1" />
              <rect x="14" y="12" width="7" height="9" rx="1" />
              <rect x="3" y="16" width="7" height="5" rx="1" />
            </svg>
          </span>
          Tableros Inteligentes
        </h1>
        <p class="page-desc">
          Organización ágil mediante tablero Kanban, reto de 21 días para consolidación de hábitos y pizarrón libre de ideas.
        </p>
      </div>

      <!-- Selector Superior de Herramientas (3 Módulos Principales) -->
      <div class="main-tools-selector glass-panel">
        <button
          type="button"
          class="tool-tab-btn"
          :class="{ active: boards.activeMainTab.value === 'activities' }"
          @click="boards.setMainTab('activities')"
        >
          <span class="tab-icon">📋</span>
          <span class="tab-label">Tablero de Actividades</span>
        </button>

        <button
          type="button"
          class="tool-tab-btn"
          :class="{ active: boards.activeMainTab.value === 'habits' }"
          @click="boards.setMainTab('habits')"
        >
          <span class="tab-icon">⚡</span>
          <span class="tab-label">Tablero de Hábitos (21 Días)</span>
        </button>

        <button
          type="button"
          class="tool-tab-btn"
          :class="{ active: boards.activeMainTab.value === 'canvas' }"
          @click="boards.setMainTab('canvas')"
        >
          <span class="tab-icon">💡</span>
          <span class="tab-label">Pizarrón de Ideas</span>
        </button>
      </div>
    </header>

    <!-- Estado No Autenticado -->
    <div v-if="!isAuthenticated" class="auth-guard-panel glass-panel">
      <span class="guard-icon">🔒</span>
      <h2 class="guard-title">Acceso Exclusivo Protegido</h2>
      <p class="guard-desc">
        Debes iniciar sesión con tu cuenta de Google para acceder a tus tableros Kanban, seguimiento de hábitos y pizarrón de ideas.
      </p>
      <NuxtLink to="/login" class="login-btn glow-blue">
        Iniciar Sesión con Google
      </NuxtLink>
    </div>

    <!-- Contenido Autenticado -->
    <div v-else class="boards-content-area">
      <!-- ═══════════════════════════════════════════════════════════ -->
      <!-- HERRAMIENTA 1: TABLERO DE ACTIVIDADES                       -->
      <!-- ═══════════════════════════════════════════════════════════ -->
      <div v-if="boards.activeMainTab.value === 'activities'" class="activities-subview-wrapper">
        <!-- Sub-navegación: Tablero Activo | Backlog | Finalizados (+7d) -->
        <div class="sub-nav-bar glass-panel">
          <div class="sub-nav-tabs">
            <button
              class="sub-nav-btn"
              :class="{ active: boards.activeActivityView.value === 'kanban' }"
              @click="boards.setActivityView('kanban')"
            >
              <span>📌</span> Tablero Activo
              <span v-if="boards.kanban.value" class="nav-count-pill">
                {{ boards.kanban.value.total_active }}
              </span>
            </button>

            <button
              class="sub-nav-btn"
              :class="{ active: boards.activeActivityView.value === 'backlog' }"
              @click="boards.setActivityView('backlog')"
            >
              <span>📥</span> Backlog
              <span class="nav-count-pill">
                {{ boards.backlogTasks.value.length }}
              </span>
            </button>

            <button
              class="sub-nav-btn"
              :class="{ active: boards.activeActivityView.value === 'archived' }"
              @click="boards.setActivityView('archived')"
            >
              <span>🗄️</span> Finalizados (+7 días)
              <span v-if="boards.kanban.value?.archived_count" class="nav-count-pill archived">
                {{ boards.kanban.value.archived_count }}
              </span>
            </button>
          </div>
        </div>

        <!-- Vista 1.1: Tablero Kanban (4 Columnas) -->
        <KanbanBoardView
          v-if="boards.activeActivityView.value === 'kanban'"
          :kanban="boards.kanban.value"
          :epics="boards.epics.value"
          :selected-epic-id="boards.selectedEpicId.value"
          :selected-type-filter="boards.selectedTypeFilter.value"
          :search-query="boards.searchQuery.value"
          :loading="boards.loading.value"
          @update-filters="(epId, typeF, q) => boards.setFilters(epId, typeF, q)"
          @move-task="(tId, st) => handleMoveTaskStatus(tId, st)"
          @edit-task="handleOpenEditTask"
          @delete-task="handleDeleteTask"
          @move-to-backlog="handleMoveToBacklog"
          @new-task="handleOpenNewTask"
          @open-epic-manager="showEpicModal = true"
        />

        <!-- Vista 1.2: Backlog -->
        <BacklogListView
          v-else-if="boards.activeActivityView.value === 'backlog'"
          :tasks="boards.backlogTasks.value"
          :epics="boards.epics.value"
          :selected-epic-id="boards.selectedEpicId.value"
          :selected-type-filter="boards.selectedTypeFilter.value"
          :search-query="boards.searchQuery.value"
          :loading="boards.loading.value"
          @update-filters="(epId, typeF, q) => boards.setFilters(epId, typeF, q)"
          @move-to-board="handleMoveToBoard"
          @edit-task="handleOpenEditTask"
          @delete-task="handleDeleteTask"
          @new-task="handleOpenNewTask('TODO')"
        />

        <!-- Vista 1.3: Finalizados (+7 días) -->
        <ArchivedDoneView
          v-else-if="boards.activeActivityView.value === 'archived'"
          :tasks="boards.archivedTasks.value"
          :epics="boards.epics.value"
          :selected-epic-id="boards.selectedEpicId.value"
          :search-query="boards.searchQuery.value"
          :loading="boards.loading.value"
          @update-filters="(epId, q) => boards.setFilters(epId, '', q)"
          @edit-task="handleOpenEditTask"
          @delete-task="handleDeleteTask"
        />
      </div>

      <!-- ═══════════════════════════════════════════════════════════ -->
      <!-- HERRAMIENTA 2: TABLERO DE HÁBITOS (21 DÍAS)                 -->
      <!-- ═══════════════════════════════════════════════════════════ -->
      <HabitsBoardView
        v-else-if="boards.activeMainTab.value === 'habits'"
        :habits="boards.habits.value"
        :loading="boards.loading.value"
        @check-day="handleCheckHabitDay"
        @edit-habit="handleOpenEditHabit"
        @delete-habit="handleDeleteHabit"
        @new-habit="handleOpenNewHabit"
      />

      <!-- ═══════════════════════════════════════════════════════════ -->
      <!-- HERRAMIENTA 3: PIZARRÓN DE IDEAS                            -->
      <!-- ═══════════════════════════════════════════════════════════ -->
      <StickyNotesCanvas
        v-else-if="boards.activeMainTab.value === 'canvas'"
        :notes="boards.stickyNotes.value"
        :loading="boards.loading.value"
        @create-note="handleCreateNote"
        @update-note="handleUpdateNote"
        @update-position="handleUpdateNotePosition"
        @delete-note="handleDeleteNote"
      />
    </div>

    <!-- Modales Globales del Módulo -->
    <TaskModal
      :show="showTaskModal"
      :epics="boards.epics.value"
      :task-to-edit="taskToEdit"
      :default-status="defaultTaskStatus"
      :loading="modalLoading"
      @close="showTaskModal = false"
      @save="handleSaveTask"
    />

    <EpicManagerModal
      :show="showEpicModal"
      :epics="boards.epics.value"
      :loading="modalLoading"
      @close="showEpicModal = false"
      @create="handleCreateEpic"
      @delete="handleDeleteEpic"
    />

    <HabitModal
      :show="showHabitModal"
      :habit-to-edit="habitToEdit"
      :loading="modalLoading"
      @close="showHabitModal = false"
      @save="handleSaveHabit"
    />
  </div>
</template>

<style scoped>
.boards-page-container {
  display: flex;
  flex-direction: column;
  gap: 22px;
  max-width: 1560px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.boards-header {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.title-meta-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.65rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
  letter-spacing: -0.02em;
}

.title-icon {
  display: flex;
}

.page-desc {
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.92rem;
  margin: 0;
  line-height: 1.45;
}

/* Selector de 3 Herramientas Principales */
.main-tools-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px;
  border-radius: 16px;
  background: rgba(23, 23, 28, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  width: fit-content;
  flex-wrap: wrap;
}

.tool-tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 12px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--hermes-text-muted, #94949E);
  font-weight: 700;
  font-size: 0.88rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.tool-tab-btn:hover {
  color: var(--hermes-text-primary, #F4F4F5);
  background: rgba(255, 255, 255, 0.04);
}

.tool-tab-btn.active {
  background: rgba(0, 229, 255, 0.12);
  border-color: rgba(0, 229, 255, 0.3);
  color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 16px rgba(0, 229, 255, 0.15);
}

.tab-icon {
  font-size: 1.1rem;
}

/* Sub-navegación para Actividades */
.activities-subview-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sub-nav-bar {
  display: flex;
  align-items: center;
  padding: 6px 10px;
  border-radius: 14px;
  width: fit-content;
}

.sub-nav-tabs {
  display: flex;
  align-items: center;
  gap: 6px;
}

.sub-nav-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border-radius: 10px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sub-nav-btn:hover {
  color: var(--hermes-text-primary, #F4F4F5);
  background: rgba(255, 255, 255, 0.04);
}

.sub-nav-btn.active {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.12);
  color: var(--hermes-text-primary, #F4F4F5);
}

.nav-count-pill {
  font-size: 0.7rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  padding: 1px 6px;
  border-radius: 6px;
  background: rgba(0, 229, 255, 0.15);
  color: var(--hermes-accent-blue, #00E5FF);
}

.nav-count-pill.archived {
  background: rgba(0, 255, 198, 0.15);
  color: var(--hermes-accent-teal, #00FFC6);
}

/* Auth Guard */
.auth-guard-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 24px;
  text-align: center;
  border-radius: 20px;
}

.guard-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.guard-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin-bottom: 8px;
}

.guard-desc {
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.95rem;
  max-width: 480px;
  margin-bottom: 24px;
  line-height: 1.5;
}

.login-btn {
  display: inline-flex;
  align-items: center;
  padding: 12px 24px;
  border-radius: 12px;
  background: var(--hermes-accent-blue, #00E5FF);
  color: #0c0c0e;
  font-weight: 800;
  font-size: 0.95rem;
  text-decoration: none;
  transition: all 0.2s ease;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
}
</style>

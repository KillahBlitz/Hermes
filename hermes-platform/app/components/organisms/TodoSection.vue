<script setup lang="ts">
import { computed, ref } from 'vue'
import type { TodoSection, TodoTask } from '~/composables/useLists'
import TodoSectionSidebar from '~/components/molecules/TodoSectionSidebar.vue'
import TodoTaskRow from '~/components/molecules/TodoTaskRow.vue'

const props = defineProps<{
  sections: TodoSection[]
  tasks: TodoTask[]
  selectedSectionId: string
  searchQuery: string
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'selectSection', sectionId: string): void
  (e: 'updateSearch', search: string): void
  (e: 'createQuickTask', payload: { title: string; section_id?: string }): void
  (e: 'toggleTask', task: TodoTask): void
  (e: 'editTask', task: TodoTask): void
  (e: 'deleteTask', task: TodoTask): void
  (e: 'newSection'): void
  (e: 'editSection', section: TodoSection): void
  (e: 'deleteSection', section: TodoSection): void
}>()

const quickTitle = ref('')
const showCompletedAccordion = ref(true)

const currentSection = computed(() => {
  return props.sections.find(s => s.id === props.selectedSectionId)
})

const pendingTasks = computed(() => {
  return props.tasks.filter(t => !t.is_completed)
})

const completedTasks = computed(() => {
  return props.tasks.filter(t => t.is_completed)
})

const totalPending = computed(() => {
  return props.sections.reduce((acc, s) => acc + (s.pending_count || 0), 0)
})

const handleQuickSubmit = () => {
  if (!quickTitle.value.trim()) return
  emit('createQuickTask', {
    title: quickTitle.value.trim(),
    section_id: props.selectedSectionId || undefined
  })
  quickTitle.value = ''
}
</script>

<template>
  <div class="todo-section-container">
    <!-- Barra Lateral de Secciones -->
    <TodoSectionSidebar
      :sections="sections"
      :selected-section-id="selectedSectionId"
      :total-pending="totalPending"
      @select="emit('selectSection', $event)"
      @new-section="emit('newSection')"
      @edit-section="emit('editSection', $event)"
      @delete-section="emit('deleteSection', $event)"
    />

    <!-- Área Principal de Tareas -->
    <div class="todo-main-pane glass-panel">
      <!-- Header de la Sección Activa -->
      <div class="main-pane-header">
        <div class="header-titles">
          <h2 class="current-section-title">
            <span class="sec-emoji">{{ currentSection ? currentSection.icon : '📋' }}</span>
            <span>{{ currentSection ? currentSection.name : 'Todas las Tareas' }}</span>
          </h2>
          <span class="pending-badge">{{ pendingTasks.length }} pendientes</span>
        </div>

        <!-- Buscador To-Do -->
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input
            :value="searchQuery"
            type="text"
            placeholder="Buscar tarea..."
            class="search-input"
            @input="emit('updateSearch', ($event.target as HTMLInputElement).value)"
          />
        </div>
      </div>

      <!-- Quick Add Input (Tipo Microsoft To-Do) -->
      <div class="quick-add-box glass-panel">
        <span class="add-circle-hint">+</span>
        <input
          v-model="quickTitle"
          type="text"
          placeholder="Agregar una tarea (Presiona Enter)..."
          maxlength="160"
          class="quick-add-input"
          @keydown.enter.prevent="handleQuickSubmit"
        />
        <button
          type="button"
          class="quick-submit-btn glow-teal"
          :disabled="!quickTitle.trim()"
          @click="handleQuickSubmit"
        >
          Agregar
        </button>
      </div>

      <!-- Lista de Tareas Pendientes -->
      <div class="tasks-scroll-area">
        <div v-if="loading" class="skeletons-list">
          <div v-for="i in 3" :key="i" class="row-skeleton shimmer"></div>
        </div>

        <div v-else-if="pendingTasks.length === 0 && completedTasks.length === 0" class="empty-state">
          <span class="empty-icon">☀️</span>
          <h3 class="empty-title">Todo al día</h3>
          <p class="empty-desc">No hay tareas pendientes en esta lista. Escribe arriba para agregar una nueva tarea.</p>
        </div>

        <div v-else class="tasks-rows-group">
          <!-- Tareas Pendientes -->
          <TodoTaskRow
            v-for="task in pendingTasks"
            :key="task.id"
            :task="task"
            @toggle="emit('toggleTask', task)"
            @edit="emit('editTask', task)"
            @delete="emit('deleteTask', task)"
          />

          <!-- Acordeón de Tareas Completadas -->
          <div v-if="completedTasks.length > 0" class="completed-accordion">
            <button
              type="button"
              class="accordion-toggle-btn"
              @click="showCompletedAccordion = !showCompletedAccordion"
            >
              <span class="arrow-indicator">{{ showCompletedAccordion ? '▼' : '▶' }}</span>
              <span>Completadas ({{ completedTasks.length }})</span>
            </button>

            <div v-if="showCompletedAccordion" class="completed-tasks-list">
              <TodoTaskRow
                v-for="task in completedTasks"
                :key="task.id"
                :task="task"
                @toggle="emit('toggleTask', task)"
                @edit="emit('editTask', task)"
                @delete="emit('deleteTask', task)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.todo-section-container {
  display: flex;
  gap: 18px;
  align-items: flex-start;
}

.todo-main-pane {
  flex: 1;
  border-radius: 16px;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: rgba(23, 23, 28, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  min-height: 520px;
}

.main-pane-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
}

.header-titles {
  display: flex;
  align-items: center;
  gap: 12px;
}

.current-section-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.sec-emoji {
  font-size: 1.2rem;
}

.pending-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 8px;
  background: rgba(0, 229, 255, 0.1);
  color: var(--hermes-accent-blue, #00E5FF);
  border: 1px solid rgba(0, 229, 255, 0.25);
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  min-width: 200px;
}

.search-icon {
  position: absolute;
  left: 10px;
  font-size: 0.78rem;
  opacity: 0.6;
  pointer-events: none;
}

.search-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 7px 12px 7px 30px;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.82rem;
  outline: none;
}

/* Quick Add Box */
.quick-add-box {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 14px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.2s ease;
}

.quick-add-box:focus-within {
  border-color: var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 0 16px rgba(0, 255, 198, 0.15);
  background: rgba(0, 255, 198, 0.02);
}

.add-circle-hint {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--hermes-text-muted, #94949E);
  line-height: 1;
}

.quick-add-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.92rem;
  font-weight: 500;
}

.quick-add-input::placeholder {
  color: var(--hermes-text-muted, #94949E);
  opacity: 0.6;
}

.quick-submit-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  font-weight: 800;
  font-size: 0.78rem;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-submit-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* Scroll Area */
.tasks-scroll-area {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tasks-rows-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.completed-accordion {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.accordion-toggle-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  padding: 4px 0;
}

.accordion-toggle-btn:hover {
  color: var(--hermes-text-primary, #F4F4F5);
}

.arrow-indicator {
  font-size: 0.65rem;
}

.completed-tasks-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeletons-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.row-skeleton {
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
}

.shimmer {
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.02) 25%, rgba(255, 255, 255, 0.06) 50%, rgba(255, 255, 255, 0.02) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.6s infinite;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: var(--hermes-accent-teal, #00FFC6);
}

.empty-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin-bottom: 6px;
}

.empty-desc {
  font-size: 0.82rem;
  color: var(--hermes-text-muted, #94949E);
  max-width: 340px;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

@media (max-width: 768px) {
  .todo-section-container {
    flex-direction: column;
  }
}
</style>

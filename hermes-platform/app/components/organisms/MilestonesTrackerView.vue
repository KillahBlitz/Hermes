<script setup lang="ts">
import { computed } from 'vue'
import type { Milestone } from '~/composables/useProgress'
import MilestoneCard from '~/components/molecules/MilestoneCard.vue'

const props = defineProps<{
  milestones: Milestone[]
  selectedCategory: string
  selectedStatus: string
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'update:category', cat: string): void
  (e: 'update:status', st: string): void
  (e: 'create'): void
  (e: 'edit', milestone: Milestone): void
  (e: 'delete', milestone: Milestone): void
  (e: 'toggleTopic', milestoneId: string, topicId: string, isCompleted: boolean): void
}>()

const categories = [
  { value: '', label: 'Todos' },
  { value: 'TITULACION', label: '🎓 Titulación' },
  { value: 'CERTIFICACION', label: '☁️ Certificaciones' },
  { value: 'EXAMEN', label: '📚 Exámenes Críticos' },
  { value: 'PROYECTO', label: '🎯 Proyectos Macro' },
  { value: 'CARRERA', label: '🚀 Carrera Backend' }
]

const activeCount = computed(() => props.milestones.filter(m => m.status !== 'COMPLETED').length)
const completedCount = computed(() => props.milestones.filter(m => m.status === 'COMPLETED').length)
const urgentCount = computed(() => props.milestones.filter(m => m.days_remaining <= 7 && m.status !== 'COMPLETED').length)
</script>

<template>
  <div class="milestones-tracker-view">
    <!-- Top Stats Banner -->
    <div class="stats-banner glass-panel">
      <div class="stat-card">
        <span class="stat-label">Hitos Activos</span>
        <span class="stat-value text-accent-blue">{{ activeCount }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Completados</span>
        <span class="stat-value text-accent-teal">{{ completedCount }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">Próximos a vencer (< 7d)</span>
        <span class="stat-value" :class="{ 'text-accent-pink': urgentCount > 0 }">{{ urgentCount }}</span>
      </div>
    </div>

    <!-- Toolbar: Filters & Add Button -->
    <div class="milestones-toolbar">
      <div class="categories-filter">
        <button
          v-for="cat in categories"
          :key="cat.value"
          type="button"
          class="category-filter-btn"
          :class="{ 'is-active': selectedCategory === cat.value }"
          @click="emit('update:category', cat.value)"
        >
          {{ cat.label }}
        </button>
      </div>

      <button
        type="button"
        class="create-milestone-btn btn-neon-pink"
        @click="emit('create')"
      >
        <span class="btn-icon">＋</span>
        <span>Nuevo Hito</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading && milestones.length === 0" class="loading-state glass-panel">
      <div class="loading-spinner" />
      <p>Cargando hitos estratégicos...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="milestones.length === 0" class="empty-state glass-panel">
      <span class="empty-icon">🎯</span>
      <h3 class="empty-title">Sin hitos registrados</h3>
      <p class="empty-desc">Crea tu primer proyecto de gran escala (como Titulación de Ingeniería o Certificaciones AWS) para monitorear temarios y fechas límite.</p>
      <button
        type="button"
        class="btn-neon-blue"
        @click="emit('create')"
      >
        Crear Primer Hito
      </button>
    </div>

    <!-- Milestones Grid -->
    <div v-else class="milestones-grid">
      <MilestoneCard
        v-for="m in milestones"
        :key="m.id"
        :milestone="m"
        @edit="emit('edit', $event)"
        @delete="emit('delete', $event)"
        @toggle-topic="(mId, tId, comp) => emit('toggleTopic', mId, tId, comp)"
      />
    </div>
  </div>
</template>

<style scoped>
.milestones-tracker-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stats-banner {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  padding: 18px 24px;
  border-radius: 14px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--hermes-text-muted);
  font-weight: 600;
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 800;
  font-feature-settings: 'tnum';
  line-height: 1;
}

.text-accent-blue { color: var(--hermes-accent-blue, #00E5FF); }
.text-accent-teal { color: var(--hermes-accent-teal, #00FFC6); }
.text-accent-pink { color: var(--hermes-accent-pink, #FF007F); }

.milestones-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.categories-filter {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.category-filter-btn {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.category-filter-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-primary);
}

.category-filter-btn.is-active {
  background: rgba(0, 229, 255, 0.15);
  border-color: var(--hermes-accent-blue, #00E5FF);
  color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
}

.create-milestone-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
}

.btn-icon {
  font-size: 1.1rem;
  font-weight: 900;
}

.milestones-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  text-align: center;
  border-radius: 16px;
  background: var(--hermes-bg-surface);
  border: 1px dashed rgba(255, 255, 255, 0.12);
  gap: 12px;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(0, 229, 255, 0.15);
  border-top-color: var(--hermes-accent-blue, #00E5FF);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 3rem;
}

.empty-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
}

.empty-desc {
  margin: 0;
  max-width: 440px;
  font-size: 0.88rem;
  color: var(--hermes-text-muted);
  line-height: 1.5;
}
</style>

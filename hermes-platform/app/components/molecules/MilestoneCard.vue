<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Milestone, MilestoneTopic } from '~/composables/useProgress'
import MilestoneCountdownBadge from '~/components/atoms/MilestoneCountdownBadge.vue'
import MilestoneProgressBar from '~/components/atoms/MilestoneProgressBar.vue'

const props = defineProps<{
  milestone: Milestone
}>()

const emit = defineEmits<{
  (e: 'edit', milestone: Milestone): void
  (e: 'delete', milestone: Milestone): void
  (e: 'toggleTopic', milestoneId: string, topicId: string, isCompleted: boolean): void
}>()

const isExpanded = ref(false)

const formattedDate = computed(() => {
  if (!props.milestone.target_date) return ''
  try {
    const d = new Date(props.milestone.target_date)
    return d.toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    })
  } catch {
    return props.milestone.target_date
  }
})

const categoryLabel = computed(() => {
  const cat = props.milestone.category
  switch (cat) {
    case 'TITULACION': return '🎓 Titulación'
    case 'CERTIFICACION': return '☁️ Certificación'
    case 'EXAMEN': return '📚 Examen Crítico'
    case 'CARRERA': return '🚀 Carrera'
    default: return '🎯 Proyecto'
  }
})

const handleToggleTopic = (topic: MilestoneTopic) => {
  emit('toggleTopic', props.milestone.id, topic.id, !topic.is_completed)
}
</script>

<template>
  <div
    class="milestone-card glass-panel"
    :class="{
      'is-completed': milestone.status === 'COMPLETED',
      'is-overdue': milestone.is_overdue
    }"
    :style="{ '--accent-color': milestone.color || '#00FFC6' }"
  >
    <!-- Header: Category & Countdown -->
    <div class="card-top">
      <span class="category-pill">{{ categoryLabel }}</span>
      <MilestoneCountdownBadge
        :days-remaining="milestone.days_remaining"
        :is-overdue="milestone.is_overdue"
        :is-completed="milestone.status === 'COMPLETED'"
      />
    </div>

    <!-- Title & Description -->
    <div class="card-main">
      <div class="title-row">
        <span class="milestone-icon">{{ milestone.icon || '🎯' }}</span>
        <h3 class="milestone-title">{{ milestone.title }}</h3>
      </div>
      <p v-if="milestone.description" class="milestone-desc">{{ milestone.description }}</p>
    </div>

    <!-- Target Date -->
    <div class="date-row">
      <span class="date-label">📅 Meta:</span>
      <span class="date-val">{{ formattedDate }}</span>
    </div>

    <!-- Progress Bar -->
    <div class="progress-section">
      <MilestoneProgressBar
        :percentage="milestone.progress_percentage"
        :total-topics="milestone.total_topics"
        :completed-topics="milestone.completed_topics"
        :color="milestone.color"
      />
    </div>

    <!-- Topics Checklist Preview / Collapsible -->
    <div v-if="milestone.topics && milestone.topics.length > 0" class="topics-section">
      <button
        type="button"
        class="topics-toggle-btn"
        @click="isExpanded = !isExpanded"
      >
        <span>Temario y Entregables ({{ milestone.completed_topics }}/{{ milestone.total_topics }})</span>
        <svg
          class="chevron-icon"
          :class="{ 'is-open': isExpanded }"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      <div v-if="isExpanded" class="topics-list">
        <div
          v-for="topic in milestone.topics"
          :key="topic.id"
          class="topic-item"
          :class="{ 'is-checked': topic.is_completed }"
          @click="handleToggleTopic(topic)"
        >
          <button
            type="button"
            class="topic-checkbox"
            :class="{ 'is-checked': topic.is_completed }"
          >
            <span v-if="topic.is_completed">✓</span>
          </button>
          <span class="topic-title">{{ topic.title }}</span>
        </div>
      </div>
    </div>

    <!-- Footer Actions -->
    <div class="card-actions">
      <button
        type="button"
        class="action-btn edit-btn"
        title="Editar hito"
        @click="emit('edit', milestone)"
      >
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
        </svg>
        <span>Editar</span>
      </button>
      <button
        type="button"
        class="action-btn delete-btn"
        title="Eliminar hito"
        @click="emit('delete', milestone)"
      >
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6" />
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.milestone-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 20px;
  border-radius: 16px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.milestone-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--accent-color, #00FFC6);
  opacity: 0.8;
  box-shadow: 0 0 10px var(--accent-color, #00FFC6);
}

.milestone-card:hover {
  border-color: rgba(0, 229, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.milestone-card.is-completed {
  border-color: rgba(0, 255, 198, 0.25);
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.category-pill {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--hermes-text-muted);
  background: rgba(255, 255, 255, 0.05);
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.card-main {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.milestone-icon {
  font-size: 1.3rem;
  flex-shrink: 0;
}

.milestone-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
  line-height: 1.3;
}

.milestone-desc {
  margin: 0;
  font-size: 0.82rem;
  color: var(--hermes-text-muted);
  line-height: 1.4;
}

.date-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
}

.date-label {
  color: var(--hermes-text-muted);
}

.date-val {
  color: var(--hermes-text-primary);
  font-weight: 600;
}

.topics-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  padding: 10px 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.topics-toggle-btn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: none;
  border: none;
  color: var(--hermes-text-muted);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  width: 100%;
}

.topics-toggle-btn:hover {
  color: var(--hermes-accent-blue, #00E5FF);
}

.chevron-icon {
  transition: transform 0.2s ease;
}

.chevron-icon.is-open {
  transform: rotate(180deg);
}

.topics-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 6px;
}

.topic-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 6px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.topic-item:hover {
  background: rgba(255, 255, 255, 0.04);
}

.topic-checkbox {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0c0c0e;
  font-size: 0.65rem;
  font-weight: 900;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.topic-checkbox.is-checked {
  background: var(--hermes-accent-teal, #00FFC6);
  border-color: var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 0 8px rgba(0, 255, 198, 0.4);
}

.topic-title {
  font-size: 0.8rem;
  color: var(--hermes-text-primary);
  line-height: 1.3;
}

.topic-item.is-checked .topic-title {
  color: var(--hermes-text-muted);
  text-decoration: line-through;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
  margin-top: auto;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.edit-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-primary);
}

.edit-btn:hover {
  background: rgba(0, 229, 255, 0.15);
  border-color: rgba(0, 229, 255, 0.4);
  color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
}

.delete-btn {
  background: rgba(255, 77, 77, 0.08);
  border: 1px solid rgba(255, 77, 77, 0.2);
  color: #ff4d4d;
  padding: 6px 10px;
}

.delete-btn:hover {
  background: rgba(255, 77, 77, 0.22);
  border-color: #ff4d4d;
  box-shadow: 0 0 10px rgba(255, 77, 77, 0.25);
}
</style>

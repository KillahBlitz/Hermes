<script setup lang="ts">
import type { EmailSummary } from '~/composables/useGmailService'

const props = defineProps<{
  email: EmailSummary
}>()

const emit = defineEmits<{
  (e: 'click'): void
  (e: 'delete'): void
}>()

const initial = computed(() => {
  return (props.email.sender || props.email.sender_email || 'U').charAt(0).toUpperCase()
})

const formattedDate = computed(() => {
  if (!props.email.date) return ''
  try {
    const d = new Date(props.email.date)
    return d.toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return props.email.date
  }
})
</script>

<template>
  <div class="email-card glass-panel" @click="emit('click')">
    <!-- Left: Sender Avatar -->
    <div class="sender-avatar-ring">
      <span class="sender-avatar-initial">{{ initial }}</span>
    </div>

    <!-- Center: Email Info -->
    <div class="email-content">
      <div class="email-header-row">
        <span class="sender-name">{{ email.sender }}</span>
        <div class="email-badges">
          <span v-if="email.is_starred" class="badge-tag badge-starred" title="Destacado">
            ⭐ Destacado
          </span>
          <span v-if="email.is_important" class="badge-tag badge-important" title="Importante">
            🏷️ Importante
          </span>
        </div>
        <span class="email-date">{{ formattedDate }}</span>
      </div>

      <div class="email-subject">
        {{ email.subject }}
      </div>

      <div class="email-snippet">
        {{ email.snippet }}
      </div>
    </div>

    <!-- Right: Quick Actions -->
    <div class="email-actions" @click.stop>
      <button
        class="action-btn delete-btn"
        title="Eliminar correo"
        type="button"
        @click="emit('delete')"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="3 6 5 6 21 6" />
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.email-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px 20px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.email-card:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(0, 229, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.sender-avatar-ring {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  padding: 2px;
  background: linear-gradient(135deg, var(--hermes-accent-blue), var(--hermes-accent-pink));
  flex-shrink: 0;
}

.sender-avatar-initial {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--hermes-bg-surface);
  color: var(--hermes-accent-blue);
  font-weight: 700;
  font-size: 0.95rem;
}

.email-content {
  flex: 1;
  min-width: 0;
}

.email-header-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 4px;
  flex-wrap: wrap;
}

.sender-name {
  font-weight: 700;
  color: var(--hermes-text-primary);
  font-size: 0.95rem;
}

.email-badges {
  display: flex;
  align-items: center;
  gap: 6px;
}

.badge-tag {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  letter-spacing: 0.02em;
}

.badge-starred {
  background: rgba(245, 158, 11, 0.15);
  color: #FBBF24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.badge-important {
  background: rgba(0, 229, 255, 0.12);
  color: var(--hermes-accent-blue);
  border: 1px solid rgba(0, 229, 255, 0.25);
}

.email-date {
  margin-left: auto;
  font-size: 0.78rem;
  color: var(--hermes-text-muted);
}

.email-subject {
  font-weight: 600;
  color: #E4E4E7;
  font-size: 0.9rem;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.email-snippet {
  color: var(--hermes-text-muted);
  font-size: 0.82rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.email-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  opacity: 0;
  transition: opacity 0.2s ease;
  flex-shrink: 0;
}

.email-card:hover .email-actions {
  opacity: 1;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: scale(1.08);
}

.delete-btn:hover {
  background: rgba(255, 0, 127, 0.15);
  border-color: rgba(255, 0, 127, 0.4);
  color: var(--hermes-accent-pink);
}
</style>

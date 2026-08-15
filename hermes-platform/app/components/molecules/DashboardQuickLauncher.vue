<script setup lang="ts">
const emit = defineEmits<{
  (e: 'quick-event'): void
  (e: 'quick-transaction'): void
  (e: 'quick-task'): void
  (e: 'quick-note'): void
}>()
</script>

<template>
  <div class="quick-launcher-bar glass-panel">
    <div class="launcher-header">
      <span class="launcher-icon">⚡</span>
      <span class="launcher-title">Acciones Rápidas</span>
    </div>

    <div class="launcher-buttons">
      <NuxtLink to="/services" class="launcher-btn btn-neon-blue">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
          <line x1="16" y1="2" x2="16" y2="6" />
          <line x1="8" y1="2" x2="8" y2="6" />
          <line x1="3" y1="10" x2="21" y2="10" />
        </svg>
        <span>Agendar Evento</span>
      </NuxtLink>

      <NuxtLink to="/finance" class="launcher-btn btn-neon-teal">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="1" x2="12" y2="23" />
          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
        </svg>
        <span>Registrar Gasto</span>
      </NuxtLink>

      <NuxtLink to="/boards" class="launcher-btn btn-neon-pink">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="7" height="9" />
          <rect x="14" y="3" width="7" height="5" />
          <rect x="14" y="12" width="7" height="9" />
          <rect x="3" y="16" width="7" height="5" />
        </svg>
        <span>Nueva Tarea Kanban</span>
      </NuxtLink>

      <NuxtLink to="/progress" class="launcher-btn btn-neon-blue">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="16" y1="13" x2="8" y2="13" />
          <line x1="16" y1="17" x2="8" y2="17" />
        </svg>
        <span>Apuntes Zettelkasten</span>
      </NuxtLink>
    </div>
  </div>
</template>

<style scoped>
.quick-launcher-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  border-radius: 14px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
  flex-wrap: wrap;
  gap: 12px;
}

.launcher-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.launcher-icon {
  font-size: 1.1rem;
  color: var(--hermes-accent-blue);
}

.launcher-title {
  font-size: 0.84rem;
  font-weight: 800;
  color: var(--hermes-text-primary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.launcher-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.launcher-btn {
  text-decoration: none;
  font-size: 0.78rem;
  padding: 7px 14px;
}
</style>

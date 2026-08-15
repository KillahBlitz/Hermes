<script setup lang="ts">
useHead({
  title: 'Tableros | Hermes',
  meta: [{ name: 'description', content: 'Tableros Kanban y gestión visual de flujos de trabajo.' }]
})
</script>

<template>
  <div class="module-page">
    <h1 class="page-title">
      <span class="title-icon text-accent-blue">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="7" height="9" rx="1" />
          <rect x="14" y="3" width="7" height="5" rx="1" />
          <rect x="14" y="12" width="7" height="9" rx="1" />
          <rect x="3" y="16" width="7" height="5" rx="1" />
        </svg>
      </span>
      Tableros
    </h1>
    <p class="page-desc">Gestión visual de flujos de trabajo mediante tableros dinámicos tipo Kanban y seguimiento ágil.</p>
    <div class="coming-soon glass-panel">
      <span class="cs-icon">📋</span>
      <p class="cs-text">Este módulo está en desarrollo.</p>
    </div>
  </div>
</template>

<style scoped>
.module-page { max-width: 800px; }
.page-title {
  display: flex; align-items: center; gap: 12px;
  font-size: 1.6rem; font-weight: 800; color: var(--hermes-text-primary); margin-bottom: 8px;
}
.title-icon { display: flex; }
.page-desc { color: var(--hermes-text-muted); font-size: 0.95rem; margin-bottom: 32px; line-height: 1.5; }
.coming-soon {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 48px 24px; text-align: center; border-radius: 16px;
}
.cs-icon { font-size: 2.5rem; margin-bottom: 12px; }
.cs-text { color: var(--hermes-text-muted); font-size: 0.9rem; margin: 0; }
</style>

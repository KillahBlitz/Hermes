<script setup lang="ts">
useHead({
  title: 'Listas | Hermes',
  meta: [{ name: 'description', content: 'Listas de verificación, tareas y notas rápidas.' }]
})
</script>

<template>
  <div class="module-page">
    <h1 class="page-title">
      <span class="title-icon text-accent-pink">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <line x1="10" y1="6" x2="21" y2="6" />
          <line x1="10" y1="12" x2="21" y2="12" />
          <line x1="10" y1="18" x2="21" y2="18" />
          <polyline points="3 6 4 7 6 5" />
          <polyline points="3 12 4 13 6 11" />
          <polyline points="3 18 4 19 6 17" />
        </svg>
      </span>
      Listas
    </h1>
    <p class="page-desc">Listas de verificación, tareas pendientes (To-Do), notas rápidas y categorización por prioridades.</p>
    <div class="coming-soon glass-panel">
      <span class="cs-icon">✅</span>
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

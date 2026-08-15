<script setup lang="ts">
useHead({
  title: 'Progreso Profesional | Hermes',
  meta: [{ name: 'description', content: 'Tracker de desarrollo profesional, metas y habilidades.' }]
})
</script>

<template>
  <div class="module-page">
    <h1 class="page-title">
      <span class="title-icon text-accent-pink">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" />
          <path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" />
          <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0" />
          <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5" />
        </svg>
      </span>
      Progreso Profesional
    </h1>
    <p class="page-desc">Metas trimestrales, árbol de habilidades (skills tracker), cursos y certificaciones.</p>
    <div class="coming-soon glass-panel">
      <span class="cs-icon">🎯</span>
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

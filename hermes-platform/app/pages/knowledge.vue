<script setup lang="ts">
useHead({
  title: 'Conocimiento | Hermes',
  meta: [{ name: 'description', content: 'Base de conocimiento, notas interconectadas y documentación.' }]
})
</script>

<template>
  <div class="module-page">
    <h1 class="page-title">
      <span class="title-icon text-accent-teal">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
          <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
        </svg>
      </span>
      Conocimiento
    </h1>
    <p class="page-desc">Segundo cerebro ("Second Brain"), notas interconectadas en Markdown, snippets de código y documentación.</p>
    <div class="coming-soon glass-panel">
      <span class="cs-icon">🧠</span>
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

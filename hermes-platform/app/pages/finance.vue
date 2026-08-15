<script setup lang="ts">
useHead({
  title: 'Administración Económica | Hermes',
  meta: [{ name: 'description', content: 'Control financiero, presupuestos y balances.' }]
})
</script>

<template>
  <div class="module-page">
    <h1 class="page-title">
      <span class="title-icon text-accent-teal">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="20" x2="12" y2="10" />
          <line x1="18" y1="20" x2="18" y2="4" />
          <line x1="6" y1="20" x2="6" y2="16" />
        </svg>
      </span>
      Administración Económica
    </h1>
    <p class="page-desc">Registro de ingresos y egresos, métricas de ahorro, gráficos interactivos y balances financieros.</p>
    <div class="coming-soon glass-panel">
      <span class="cs-icon">💰</span>
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

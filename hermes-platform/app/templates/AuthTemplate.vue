<script setup lang="ts">
import HermesLogo from '~/components/atoms/HermesLogo.vue'
import HermesParticles from '~/components/atoms/HermesParticles.vue'

interface Props {
  title?: string
  subtitle?: string
}

withDefaults(defineProps<Props>(), {
  title: 'Bienvenido a Hermes',
  subtitle: 'Inicia sesión para gestionar tus herramientas de productividad e integraciones.',
})
</script>

<template>
  <div class="auth-wrapper">
    <!-- Ambient Background with dynamic blue/pink neon animations -->
    <div class="ambient-background">
      <div class="ambient-grid" />
      <div class="ambient-orb ambient-orb-blue" />
      <div class="ambient-orb ambient-orb-pink" />
      <div class="ambient-orb ambient-orb-teal" />
      <HermesParticles :particle-count="55" />
    </div>

    <!-- Centered Glass Panel Card -->
    <main class="auth-container">
      <div class="glass-panel glass-panel-glow p-4 p-md-5">
        <!-- Brand Header -->
        <header class="text-center mb-4">
          <div class="logo-hero-container mb-3">
            <HermesLogo size="lg" :animated="true" :glow="true" />
          </div>

          <div class="brand-badge mb-3">
            <span class="brand-dot-blue" />
            <span class="brand-dot-pink" />
            <span class="brand-badge-text">Hermes Platform</span>
          </div>

          <h1 class="brand-title mb-2">
            <span class="text-gradient-brand">Hermes</span>
          </h1>
          <p class="brand-subtitle text-muted">
            {{ subtitle }}
          </p>
        </header>

        <!-- Slot Content (Login, Forms, Buttons) -->
        <slot />

        <!-- Footer / Scopes info -->
        <footer class="auth-footer mt-4 pt-3 border-top border-secondary border-opacity-10 text-center">
          <slot name="footer">
            <p class="small text-muted mb-0">
              Conexión cifrada de extremo a extremo mediante Firebase & Google OAuth 2.0
            </p>
          </slot>
        </footer>
      </div>
    </main>
  </div>
</template>

<style scoped>
.auth-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  position: relative;
}

.auth-container {
  width: 100%;
  max-width: 480px;
  position: relative;
  z-index: 10;
}

.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 14px;
  border-radius: 100px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.brand-dot-blue {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--hermes-accent-blue);
  box-shadow: 0 0 10px var(--hermes-accent-blue);
}

.brand-dot-pink {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--hermes-accent-pink);
  box-shadow: 0 0 10px var(--hermes-accent-pink);
}

.brand-badge-text {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--hermes-text-muted);
}

.brand-title {
  font-size: 2.1rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.15;
}

.brand-subtitle {
  font-size: 0.93rem;
  line-height: 1.5;
  color: var(--hermes-text-muted) !important;
}

.auth-footer {
  font-size: 0.8rem;
}
</style>

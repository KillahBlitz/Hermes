<script setup lang="ts">
useHead({
  title: 'Dashboard | Hermes Platform',
  meta: [
    { name: 'description', content: 'Panel principal de Hermes Platform.' }
  ]
})

const { user, isAuthenticated, fetchCurrentUser } = useAuth()
const router = useRouter()

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.push('/login')
  } else {
    await fetchCurrentUser()
  }
})
</script>

<template>
  <div class="dashboard-page">
    <h1 class="page-title text-gradient-brand">Dashboard</h1>
    <p class="page-subtitle">Bienvenido de vuelta, {{ user?.display_name || 'Usuario' }}.</p>

    <!-- Google Services Grid -->
    <h2 class="section-label">Servicios de Google Conectados</h2>

    <div class="services-grid">
      <!-- Google Drive -->
      <div class="service-card">
        <div class="service-card-header">
          <span class="service-icon text-accent-teal">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
              <path d="M7.71 3.5L1.15 15l3.43 6l6.55-11.5L7.71 3.5zm3.43 6l6.56 11.5H4.58l3.43-6l3.13-5.5zm5.15-6l6.56 11.5l-3.43 6l-6.56-11.5l3.43-6z"/>
            </svg>
          </span>
          <span class="status-dot dot-teal" />
        </div>
        <h3 class="service-name">Google Drive</h3>
        <p class="service-desc">Gestión de archivos y sincronización habilitada.</p>
      </div>

      <!-- Google Calendar -->
      <div class="service-card">
        <div class="service-card-header">
          <span class="service-icon text-accent-blue">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
          </span>
          <span class="status-dot dot-blue" />
        </div>
        <h3 class="service-name">Google Calendar</h3>
        <p class="service-desc">Lectura y creación de eventos activos.</p>
      </div>

      <!-- Gmail -->
      <div class="service-card">
        <div class="service-card-header">
          <span class="service-icon text-accent-pink">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
          </span>
          <span class="status-dot dot-pink" />
        </div>
        <h3 class="service-name">Gmail</h3>
        <p class="service-desc">Modificación y lectura de correos autorizada.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-page {
  max-width: 900px;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 4px;
}

.page-subtitle {
  color: var(--hermes-text-muted);
  font-size: 1rem;
  margin-bottom: 32px;
}

.section-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--hermes-text-muted);
  margin-bottom: 16px;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.service-card {
  background: rgba(23, 23, 28, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.service-card:hover {
  background: rgba(34, 34, 42, 0.7);
  border-color: rgba(255, 255, 255, 0.12);
  transform: translateY(-3px);
}

.service-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.service-icon {
  display: flex;
  align-items: center;
}

.service-name {
  font-size: 1rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
  margin: 0 0 4px;
}

.service-desc {
  font-size: 0.82rem;
  color: var(--hermes-text-muted);
  margin: 0;
  line-height: 1.45;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot-teal {
  background: var(--hermes-accent-teal);
  box-shadow: 0 0 8px var(--hermes-accent-teal);
}

.dot-blue {
  background: var(--hermes-accent-blue);
  box-shadow: 0 0 8px var(--hermes-accent-blue);
}

.dot-pink {
  background: var(--hermes-accent-pink);
  box-shadow: 0 0 8px var(--hermes-accent-pink);
}
</style>

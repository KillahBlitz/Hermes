<script setup lang="ts">
useHead({
  title: 'Configuración | Hermes',
  meta: [{ name: 'description', content: 'Configuración de cuenta y preferencias de la plataforma.' }]
})

const { user, logout, isLoading } = useAuth()
</script>

<template>
  <div class="module-page">
    <h1 class="page-title">
      <span class="title-icon text-accent-blue">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="3" />
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
        </svg>
      </span>
      Configuración
    </h1>
    <p class="page-desc">Administra tu cuenta, preferencias y sesión activa.</p>

    <!-- Session Card -->
    <div class="settings-card glass-panel">
      <h2 class="card-title">Sesión Activa</h2>
      <div class="session-info">
        <div class="session-avatar-ring">
          <img
            v-if="user?.photo_url"
            :src="user.photo_url"
            :alt="user?.display_name || 'User'"
            class="session-avatar-img"
          />
          <span v-else class="session-avatar-fallback">
            {{ (user?.display_name || user?.email || 'U').charAt(0).toUpperCase() }}
          </span>
        </div>
        <div class="session-details">
          <p class="session-name">{{ user?.display_name || 'Usuario' }}</p>
          <p class="session-email">{{ user?.email }}</p>
        </div>
      </div>
      <button
        class="logout-button"
        :disabled="isLoading"
        @click="logout"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
          <polyline points="16 17 21 12 16 7" />
          <line x1="21" y1="12" x2="9" y2="12" />
        </svg>
        {{ isLoading ? 'Cerrando...' : 'Cerrar sesión' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.module-page { max-width: 600px; }
.page-title {
  display: flex; align-items: center; gap: 12px;
  font-size: 1.6rem; font-weight: 800; color: var(--hermes-text-primary); margin-bottom: 8px;
}
.title-icon { display: flex; }
.page-desc { color: var(--hermes-text-muted); font-size: 0.95rem; margin-bottom: 32px; line-height: 1.5; }

.settings-card {
  padding: 28px;
  border-radius: 16px;
}

.card-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--hermes-text-muted);
  margin-bottom: 20px;
}

.session-info {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 24px;
}

.session-avatar-ring {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  padding: 2px;
  background: linear-gradient(135deg, var(--hermes-accent-blue), var(--hermes-accent-pink));
  flex-shrink: 0;
}

.session-avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  background: var(--hermes-bg-surface);
}

.session-avatar-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--hermes-bg-surface);
  color: var(--hermes-accent-blue);
  font-weight: 700;
  font-size: 1.1rem;
}

.session-details { min-width: 0; }
.session-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--hermes-text-primary);
}
.session-email {
  margin: 0;
  font-size: 0.82rem;
  color: var(--hermes-text-muted);
}

.logout-button {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 12px 16px;
  border: 1px solid rgba(255, 0, 127, 0.25);
  border-radius: 10px;
  background: rgba(255, 0, 127, 0.06);
  color: var(--hermes-accent-pink);
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: inherit;
}

.logout-button:hover {
  background: rgba(255, 0, 127, 0.12);
  border-color: rgba(255, 0, 127, 0.4);
  box-shadow: 0 0 16px rgba(255, 0, 127, 0.15);
}

.logout-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>

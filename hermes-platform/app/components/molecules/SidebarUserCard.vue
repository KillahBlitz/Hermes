<script setup lang="ts">
defineProps<{
  isExpanded: boolean
}>()

const { user, logout, isLoading } = useAuth()

const initials = computed(() => {
  const name = user.value?.display_name || user.value?.email || 'U'
  return name.charAt(0).toUpperCase()
})
</script>

<template>
  <div class="sidebar-user" :class="{ 'is-expanded': isExpanded }">
    <!-- Avatar -->
    <div class="user-avatar-ring">
      <img
        v-if="user?.photo_url"
        :src="user.photo_url"
        :alt="user.display_name || 'User'"
        class="user-avatar-img"
      />
      <span v-else class="user-avatar-fallback">{{ initials }}</span>
    </div>

    <!-- User info (only when expanded) -->
    <div class="user-info" v-if="isExpanded">
      <p class="user-name">{{ user?.display_name || 'Usuario' }}</p>
      <p class="user-email">{{ user?.email }}</p>
    </div>

    <!-- Logout button (only when expanded) -->
    <button
      v-if="isExpanded"
      class="logout-btn"
      title="Cerrar sesión"
      :disabled="isLoading"
      @click="logout"
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
        <polyline points="16 17 21 12 16 7" />
        <line x1="21" y1="12" x2="9" y2="12" />
      </svg>
    </button>
  </div>
</template>

<style scoped>
.sidebar-user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  transition: padding 0.3s ease;
}

.sidebar-user:not(.is-expanded) {
  justify-content: center;
  padding: 12px 0;
}

/* Avatar ring */
.user-avatar-ring {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  padding: 2px;
  background: linear-gradient(135deg, var(--hermes-accent-blue), var(--hermes-accent-pink));
  flex-shrink: 0;
  transition: box-shadow 0.3s ease;
}

.sidebar-user:hover .user-avatar-ring {
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
}

.user-avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  background: var(--hermes-bg-surface);
}

.user-avatar-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--hermes-bg-surface);
  color: var(--hermes-accent-blue);
  font-weight: 700;
  font-size: 0.85rem;
}

/* User info */
.user-info {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.user-name {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--hermes-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  margin: 0;
  font-size: 0.7rem;
  color: var(--hermes-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Logout */
.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--hermes-text-muted);
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.25s ease;
}

.logout-btn:hover {
  color: var(--hermes-accent-pink);
  background: rgba(255, 0, 127, 0.08);
}

.logout-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>

<script setup lang="ts">
import HermesSidebar from '~/components/organisms/HermesSidebar.vue'
import HermesParticles from '~/components/atoms/HermesParticles.vue'

const { isPinned, isExpanded, toggleMobile } = useSidebarState()
const { isAuthenticated } = useAuth()
const router = useRouter()

// Redirect unauthenticated users to login
onMounted(() => {
  if (!isAuthenticated.value) {
    router.push('/login')
  }
})
</script>

<template>
  <div class="layout-dashboard">
    <!-- Ambient Background with Interactive Particles -->
    <div class="ambient-background">
      <div class="ambient-grid" />
      <div class="ambient-orb ambient-orb-blue" />
      <div class="ambient-orb ambient-orb-pink" />
      <div class="ambient-orb ambient-orb-teal" />
      <HermesParticles :particle-count="40" />
    </div>

    <!-- Sidebar -->
    <HermesSidebar />

    <!-- Mobile Hamburger -->
    <button
      class="mobile-hamburger"
      @click="toggleMobile"
      aria-label="Abrir menú"
    >
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="6" x2="21" y2="6" />
        <line x1="3" y1="12" x2="21" y2="12" />
        <line x1="3" y1="18" x2="21" y2="18" />
      </svg>
    </button>

    <!-- Main Content Area -->
    <main
      class="layout-main"
      :class="{
        'main-pinned': isPinned,
        'main-collapsed': !isPinned
      }"
    >
      <slot />
    </main>
  </div>
</template>

<style scoped>
.layout-dashboard {
  min-height: 100vh;
  position: relative;
}

.layout-main {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  padding: 24px 32px;
  transition: margin-left var(--sidebar-transition);
}

.layout-main.main-pinned {
  margin-left: var(--sidebar-width-expanded);
}

.layout-main.main-collapsed {
  margin-left: var(--sidebar-width-collapsed);
}

/* Mobile hamburger */
.mobile-hamburger {
  display: none;
  position: fixed;
  top: 14px;
  left: 14px;
  z-index: 101;
  width: 42px;
  height: 42px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  background: rgba(12, 12, 14, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  color: var(--hermes-text-primary);
  cursor: pointer;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.mobile-hamburger:hover {
  background: rgba(23, 23, 28, 0.95);
}

@media (max-width: 767px) {
  .mobile-hamburger {
    display: flex;
  }

  .layout-main {
    margin-left: 0 !important;
    padding: 70px 16px 24px;
  }
}
</style>

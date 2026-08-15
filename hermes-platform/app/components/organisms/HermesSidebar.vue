<script setup lang="ts">
import HermesLogo from '~/components/atoms/HermesLogo.vue'
import SidebarPinToggle from '~/components/atoms/SidebarPinToggle.vue'
import SidebarItem from '~/components/molecules/SidebarItem.vue'
import SidebarUserCard from '~/components/molecules/SidebarUserCard.vue'

const { isPinned, isHovered, isMobileOpen, isExpanded, togglePin, setHovered, closeMobile } = useSidebarState()

const navItems = [
  {
    to: '/services',
    label: 'Administrador de servicios',
    icon: 'services'
  },
  {
    to: '/finance',
    label: 'Administración económica',
    icon: 'finance'
  },
  {
    to: '/boards',
    label: 'Tableros',
    icon: 'boards'
  },
  {
    to: '/lists',
    label: 'Listas',
    icon: 'lists'
  },
  {
    to: '/progress',
    label: 'Progreso',
    icon: 'progress'
  }
]
</script>

<template>
  <!-- Mobile Backdrop -->
  <Transition name="backdrop-fade">
    <div
      v-if="isMobileOpen"
      class="sidebar-backdrop"
      @click="closeMobile"
    />
  </Transition>

  <aside
    class="hermes-sidebar"
    :class="{
      'is-expanded': isExpanded,
      'is-pinned': isPinned,
      'is-hover-expanded': isHovered && !isPinned,
      'is-mobile-open': isMobileOpen
    }"
    @mouseenter="setHovered(true)"
    @mouseleave="setHovered(false)"
  >
    <!-- Header: Logo + Pin -->
    <div class="sidebar-header">
      <NuxtLink to="/" class="sidebar-brand" @click="closeMobile">
        <!-- New Hermes Logo -->
        <HermesLogo size="sm" :animated="true" />

        <span class="brand-text">
          <span class="brand-name">Hermes</span>
          <span class="brand-sub">Platform</span>
        </span>
      </NuxtLink>

      <SidebarPinToggle
        :is-pinned="isPinned"
        :is-expanded="isExpanded"
        @toggle="togglePin"
      />
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav">
      <SidebarItem
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        :label="item.label"
        :is-expanded="isExpanded"
        @click="closeMobile"
      >
        <template #icon>
          <!-- Services: Cloud/Network -->
          <svg v-if="item.icon === 'services'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" />
          </svg>

          <!-- Finance: Bar chart -->
          <svg v-else-if="item.icon === 'finance'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="20" x2="12" y2="10" />
            <line x1="18" y1="20" x2="18" y2="4" />
            <line x1="6" y1="20" x2="6" y2="16" />
          </svg>

          <!-- Boards: Layout/Kanban -->
          <svg v-else-if="item.icon === 'boards'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="7" height="9" rx="1" />
            <rect x="14" y="3" width="7" height="5" rx="1" />
            <rect x="14" y="12" width="7" height="9" rx="1" />
            <rect x="3" y="16" width="7" height="5" rx="1" />
          </svg>

          <!-- Lists: Check list -->
          <svg v-else-if="item.icon === 'lists'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <line x1="10" y1="6" x2="21" y2="6" />
            <line x1="10" y1="12" x2="21" y2="12" />
            <line x1="10" y1="18" x2="21" y2="18" />
            <polyline points="3 6 4 7 6 5" />
            <polyline points="3 12 4 13 6 11" />
            <polyline points="3 18 4 19 6 17" />
          </svg>

          <!-- Progress: Rocket -->
          <svg v-else-if="item.icon === 'progress' || item.icon === 'career'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" />
            <path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" />
            <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0" />
            <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5" />
          </svg>
        </template>
      </SidebarItem>
    </nav>

    <!-- Footer: Settings + User Card -->
    <div class="sidebar-footer">
      <SidebarItem
        to="/settings"
        label="Configuración"
        :is-expanded="isExpanded"
        @click="closeMobile"
      >
        <template #icon>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3" />
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
          </svg>
        </template>
      </SidebarItem>
      <SidebarUserCard :is-expanded="isExpanded" />
    </div>
  </aside>
</template>

<style scoped>
.hermes-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: var(--sidebar-width-collapsed);
  background: rgba(12, 12, 14, 0.92);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  flex-direction: column;
  z-index: 100;
  transition: width var(--sidebar-transition);
  overflow: hidden;
}

/* Expanded states */
.hermes-sidebar.is-expanded {
  width: var(--sidebar-width-expanded);
}

/* When hovering (not pinned), float over content */
.hermes-sidebar.is-hover-expanded {
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8),
              0 0 20px rgba(0, 229, 255, 0.04);
}

/* Subtle glow on right edge */
.hermes-sidebar::after {
  content: '';
  position: absolute;
  top: 20%;
  right: 0;
  width: 1px;
  height: 60%;
  background: linear-gradient(180deg, transparent, rgba(0, 229, 255, 0.15), rgba(255, 0, 127, 0.15), transparent);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.5s ease;
}

.hermes-sidebar.is-expanded::after {
  opacity: 1;
}

/* ── Header ── */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  min-height: 64px;
  flex-shrink: 0;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--hermes-text-primary);
  overflow: hidden;
}

.brand-glyph {
  flex-shrink: 0;
  filter: drop-shadow(0 0 6px rgba(0, 229, 255, 0.3));
  animation: glyphPulse 4s ease-in-out infinite alternate;
}

@keyframes glyphPulse {
  0% { filter: drop-shadow(0 0 4px rgba(0, 229, 255, 0.2)); }
  100% { filter: drop-shadow(0 0 10px rgba(0, 229, 255, 0.5)); }
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
  white-space: nowrap;
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.hermes-sidebar:not(.is-expanded) .brand-text {
  opacity: 0;
  transform: translateX(-10px);
  width: 0;
  overflow: hidden;
}

.brand-name {
  font-size: 1.05rem;
  font-weight: 800;
  background: linear-gradient(90deg, var(--hermes-accent-blue), var(--hermes-accent-pink));
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-sub {
  font-size: 0.65rem;
  font-weight: 500;
  color: var(--hermes-text-muted);
  -webkit-text-fill-color: var(--hermes-text-muted);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

/* ── Navigation ── */
.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 0;
  overflow-y: auto;
  overflow-x: hidden;
}

/* Hide scrollbar in sidebar */
.sidebar-nav::-webkit-scrollbar {
  width: 0;
}

/* ── Footer ── */
.sidebar-footer {
  flex-shrink: 0;
}

/* ── Mobile Backdrop ── */
.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 99;
}

.backdrop-fade-enter-active,
.backdrop-fade-leave-active {
  transition: opacity 0.3s ease;
}
.backdrop-fade-enter-from,
.backdrop-fade-leave-to {
  opacity: 0;
}

/* ── Mobile ── */
@media (max-width: 767px) {
  .hermes-sidebar {
    transform: translateX(-100%);
    width: var(--sidebar-width-expanded);
  }

  .hermes-sidebar.is-mobile-open {
    transform: translateX(0);
  }
}
</style>

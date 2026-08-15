<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title: string
    to: string
    subtitle?: string
    badgeText?: string
    accentColor?: 'blue' | 'pink' | 'teal' | 'yellow'
  }>(),
  {
    subtitle: '',
    badgeText: '',
    accentColor: 'blue'
  }
)
</script>

<template>
  <div class="bento-widget glass-panel glass-card-interactive" :class="`accent-${accentColor}`">
    <!-- Header -->
    <div class="widget-header">
      <div class="widget-title-group">
        <slot name="icon" />
        <div>
          <h3 class="widget-title">{{ title }}</h3>
          <span v-if="subtitle" class="widget-subtitle">{{ subtitle }}</span>
        </div>
      </div>

      <div class="header-right">
        <span v-if="badgeText" class="widget-badge">{{ badgeText }}</span>
        <NuxtLink :to="to" class="widget-link-btn" title="Ir al módulo">
          <span class="link-arrow">↗</span>
        </NuxtLink>
      </div>
    </div>

    <!-- Body -->
    <div class="widget-body">
      <slot />
    </div>

    <!-- Footer if provided -->
    <div v-if="$slots.footer" class="widget-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<style scoped>
.bento-widget {
  display: flex;
  flex-direction: column;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.bento-widget::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: transparent;
  transition: all 0.3s ease;
}

.bento-widget.accent-blue::before {
  background: linear-gradient(90deg, transparent, var(--hermes-accent-blue), transparent);
}

.bento-widget.accent-pink::before {
  background: linear-gradient(90deg, transparent, var(--hermes-accent-pink), transparent);
}

.bento-widget.accent-teal::before {
  background: linear-gradient(90deg, transparent, var(--hermes-accent-teal), transparent);
}

.bento-widget.accent-yellow::before {
  background: linear-gradient(90deg, transparent, #ffd166, transparent);
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  gap: 12px;
}

.widget-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.widget-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--hermes-text-primary);
  letter-spacing: -0.01em;
}

.widget-subtitle {
  font-size: 0.75rem;
  color: var(--hermes-text-muted);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.widget-badge {
  font-size: 0.7rem;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-primary);
  padding: 3px 8px;
  border-radius: 6px;
  text-transform: uppercase;
}

.widget-link-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--hermes-text-muted);
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.widget-link-btn:hover {
  background: rgba(0, 229, 255, 0.15);
  border-color: rgba(0, 229, 255, 0.4);
  color: var(--hermes-accent-blue);
  transform: translateY(-1px) scale(1.05);
}

.link-arrow {
  font-size: 0.95rem;
  font-weight: 900;
}

.widget-body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.widget-footer {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}
</style>

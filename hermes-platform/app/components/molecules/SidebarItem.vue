<script setup lang="ts">
import SidebarTooltip from '~/components/atoms/SidebarTooltip.vue'

const props = defineProps<{
  to: string
  label: string
  isExpanded: boolean
}>()

const route = useRoute()
const isActive = computed(() => route.path === props.to || route.path.startsWith(props.to + '/'))
const isTooltipVisible = ref(false)
</script>

<template>
  <NuxtLink
    :to="to"
    class="sidebar-item"
    :class="{ 'is-active': isActive, 'is-expanded': isExpanded }"
    @mouseenter="isTooltipVisible = true"
    @mouseleave="isTooltipVisible = false"
  >
    <!-- Active indicator pill -->
    <span class="active-pill" />

    <!-- Icon slot -->
    <span class="sidebar-item-icon">
      <slot name="icon" />
    </span>

    <!-- Label with fade transition -->
    <span class="sidebar-item-label">
      {{ label }}
    </span>

    <!-- Tooltip in collapsed mode -->
    <SidebarTooltip
      v-if="!isExpanded"
      :text="label"
      :visible="isTooltipVisible"
    />
  </NuxtLink>
</template>

<style scoped>
.sidebar-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 16px;
  margin: 2px 8px;
  border-radius: 10px;
  text-decoration: none;
  color: var(--hermes-text-muted);
  cursor: pointer;
  transition: all 0.25s ease;
  overflow: hidden;
}

.sidebar-item:hover {
  color: var(--hermes-text-primary);
  background: rgba(255, 255, 255, 0.04);
}

.sidebar-item.is-active {
  color: var(--hermes-text-primary);
  background: rgba(0, 229, 255, 0.06);
}

/* Active neon pill on left edge */
.active-pill {
  position: absolute;
  left: 0;
  top: 50%;
  width: 3px;
  height: 0;
  border-radius: 0 3px 3px 0;
  background: linear-gradient(180deg, var(--hermes-accent-blue), var(--hermes-accent-pink));
  box-shadow: 0 0 12px var(--hermes-accent-blue);
  transform: translateY(-50%);
  transition: height 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.sidebar-item.is-active .active-pill {
  height: 60%;
}

/* Icon */
.sidebar-item-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  transition: transform 0.25s ease, color 0.25s ease;
}

.sidebar-item:hover .sidebar-item-icon {
  transform: scale(1.1);
}

.sidebar-item.is-active .sidebar-item-icon {
  color: var(--hermes-accent-blue);
  filter: drop-shadow(0 0 4px rgba(0, 229, 255, 0.5));
}

/* Label with fade/slide transition when collapsing */
.sidebar-item-label {
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.sidebar-item:not(.is-expanded) .sidebar-item-label {
  opacity: 0;
  transform: translateX(-10px);
  width: 0;
  overflow: hidden;
  pointer-events: none;
}
</style>

export const useSidebarState = () => {
  const isPinned = useState<boolean>('sidebar_pinned', () => false)
  const isHovered = useState<boolean>('sidebar_hovered', () => false)
  const isMobileOpen = useState<boolean>('sidebar_mobile_open', () => false)

  const isExpanded = computed(() => isPinned.value || isHovered.value)

  // Restore persisted preference on client mount
  if (import.meta.client) {
    onMounted(() => {
      const stored = localStorage.getItem('hermes_sidebar_pinned')
      if (stored === 'true') {
        isPinned.value = true
      }
    })
  }

  const togglePin = () => {
    isPinned.value = !isPinned.value
    if (import.meta.client) {
      localStorage.setItem('hermes_sidebar_pinned', String(isPinned.value))
    }
    // When pinning, clear hover state
    if (isPinned.value) {
      isHovered.value = false
    }
  }

  const setHovered = (val: boolean) => {
    // Only allow hover-expand when NOT pinned
    if (!isPinned.value) {
      isHovered.value = val
    }
  }

  const toggleMobile = () => {
    isMobileOpen.value = !isMobileOpen.value
  }

  const closeMobile = () => {
    isMobileOpen.value = false
  }

  return {
    isPinned,
    isHovered,
    isMobileOpen,
    isExpanded,
    togglePin,
    setHovered,
    toggleMobile,
    closeMobile
  }
}

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    mimeType?: string
    isFolder?: boolean
    size?: number
  }>(),
  {
    mimeType: '',
    isFolder: false,
    size: 24
  }
)

const fileCategory = computed(() => {
  if (props.isFolder) return 'folder'
  const mime = props.mimeType.toLowerCase()
  if (mime.startsWith('image/')) return 'image'
  if (mime.startsWith('video/')) return 'video'
  if (mime.startsWith('audio/')) return 'audio'
  if (mime.includes('pdf')) return 'pdf'
  if (mime.includes('spreadsheet') || mime.includes('excel') || mime.includes('csv')) return 'sheet'
  if (mime.includes('document') || mime.includes('word') || mime.includes('text')) return 'doc'
  if (mime.includes('zip') || mime.includes('compressed') || mime.includes('tar') || mime.includes('rar')) return 'archive'
  return 'file'
})
</script>

<template>
  <span class="file-type-icon" :class="`icon-${fileCategory}`">
    <!-- Folder -->
    <svg v-if="fileCategory === 'folder'" :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
    </svg>

    <!-- Image -->
    <svg v-else-if="fileCategory === 'image'" :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <circle cx="8.5" cy="8.5" r="1.5" />
      <polyline points="21 15 16 10 5 21" />
    </svg>

    <!-- Video -->
    <svg v-else-if="fileCategory === 'video'" :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <polygon points="23 7 16 12 23 17 23 7" />
      <rect x="1" y="5" width="15" height="14" rx="2" ry="2" />
    </svg>

    <!-- Audio -->
    <svg v-else-if="fileCategory === 'audio'" :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M9 18V5l12-2v13" />
      <circle cx="6" cy="18" r="3" />
      <circle cx="18" cy="16" r="3" />
    </svg>

    <!-- PDF -->
    <svg v-else-if="fileCategory === 'pdf'" :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
      <polyline points="10 9 9 9 8 9" />
    </svg>

    <!-- Sheet -->
    <svg v-else-if="fileCategory === 'sheet'" :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2" />
      <line x1="3" y1="9" x2="21" y2="9" />
      <line x1="3" y1="15" x2="21" y2="15" />
      <line x1="9" y1="3" x2="9" y2="21" />
      <line x1="15" y1="3" x2="15" y2="21" />
    </svg>

    <!-- Document -->
    <svg v-else-if="fileCategory === 'doc'" :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
    </svg>

    <!-- Archive -->
    <svg v-else-if="fileCategory === 'archive'" :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="21 8 21 21 3 21 3 8" />
      <rect x="1" y="3" width="22" height="5" />
      <line x1="10" y1="12" x2="14" y2="12" />
    </svg>

    <!-- Generic File -->
    <svg v-else :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
      <polyline points="13 2 13 9 20 9" />
    </svg>
  </span>
</template>

<style scoped>
.file-type-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.icon-folder { color: #F59E0B; }
.icon-image { color: var(--hermes-accent-teal); }
.icon-video { color: var(--hermes-accent-pink); }
.icon-audio { color: #A78BFA; }
.icon-pdf { color: #EF4444; }
.icon-sheet { color: #10B981; }
.icon-doc { color: var(--hermes-accent-blue); }
.icon-archive { color: #FBBF24; }
.icon-file { color: var(--hermes-text-muted); }
</style>

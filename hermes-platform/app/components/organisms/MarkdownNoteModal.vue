<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { ZettelNote, BacklinkItem } from '~/composables/useProgress'
import BacklinksPanel from '~/components/molecules/BacklinksPanel.vue'

const props = defineProps<{
  show: boolean
  note: ZettelNote | null
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', noteData: {
    id?: string
    title: string
    content_md: string
    tags?: string[]
    roadmap_node_id?: string
  }): void
  (e: 'openWikilink', title: string): void
}>()

const title = ref('')
const contentMd = ref('')
const tagsStr = ref('')
const viewMode = ref<'split' | 'edit' | 'preview'>('split')

watch(() => props.note, (n) => {
  if (n) {
    title.value = n.title
    contentMd.value = n.content_md
    tagsStr.value = (n.tags || []).join(', ')
  } else {
    title.value = ''
    contentMd.value = ''
    tagsStr.value = ''
  }
}, { immediate: true })

const renderedMarkdown = computed(() => {
  if (!contentMd.value) return '<p class="empty-preview">Sin contenido escrito aún...</p>'
  
  let html = contentMd.value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>')
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    .replace(/^\- (.*$)/gim, '<li>$1</li>')
    .replace(/\n\n/gim, '</p><p>')

  html = html.replace(/\[\[(.*?)\]\]/g, (match, p1) => {
    return `<button type="button" class="wikilink-btn" data-wikilink="${p1.trim()}">🔗 ${p1.trim()}</button>`
  })

  html = html.replace(/(?<!\S)#([a-zA-Z0-9_\-]+)/g, (match, p1) => {
    return `<span class="preview-tag">#${p1}</span>`
  })

  return `<p>${html}</p>`
})

const handlePreviewClick = (e: MouseEvent) => {
  const target = (e.target as HTMLElement).closest('.wikilink-btn')
  if (target) {
    const linkTitle = target.getAttribute('data-wikilink')
    if (linkTitle) {
      emit('openWikilink', linkTitle)
    }
  }
}

const handleSave = () => {
  if (!title.value.trim()) return
  const rawTags = tagsStr.value.split(',').map(t => t.trim().replace(/^#/, '')).filter(Boolean)
  emit('save', {
    id: props.note?.id,
    title: title.value.trim(),
    content_md: contentMd.value,
    tags: rawTags,
    roadmap_node_id: props.note?.roadmap_node_id
  })
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel note-modal-card">
      <!-- Modal Top Bar -->
      <div class="modal-header">
        <div class="header-left">
          <span class="note-type-icon">📝</span>
          <input
            v-model="title"
            type="text"
            class="note-title-input"
            placeholder="Título del documento Markdown..."
            required
          >
        </div>

        <div class="header-right">
          <!-- View Switcher -->
          <div class="mode-switcher">
            <button
              type="button"
              class="mode-btn"
              :class="{ 'is-active': viewMode === 'edit' }"
              @click="viewMode = 'edit'"
            >
              Editor
            </button>
            <button
              type="button"
              class="mode-btn"
              :class="{ 'is-active': viewMode === 'split' }"
              @click="viewMode = 'split'"
            >
              Dividido
            </button>
            <button
              type="button"
              class="mode-btn"
              :class="{ 'is-active': viewMode === 'preview' }"
              @click="viewMode = 'preview'"
            >
              Vista Previa
            </button>
          </div>

          <button
            type="button"
            class="btn-neon-teal save-btn"
            @click="handleSave"
          >
            Guardar
          </button>

          <button type="button" class="close-btn" @click="emit('close')">✕</button>
        </div>
      </div>

      <!-- Tags Input -->
      <div class="tags-input-row">
        <span class="tags-label">🏷️ Tags:</span>
        <input
          v-model="tagsStr"
          type="text"
          class="tags-input"
          placeholder="ej. golang, microservicios, aws (separados por coma)"
        >
      </div>

      <!-- Main Workspace -->
      <div class="workspace-body" :class="`mode-${viewMode}`">
        <!-- Editor Pane -->
        <div v-show="viewMode === 'edit' || viewMode === 'split'" class="pane-wrapper">
          <textarea
            v-model="contentMd"
            class="editor-textarea"
            placeholder="Escribe tus apuntes y bitácoras técnicas en Markdown...&#10;&#10;Usa [[Nombre de Otra Nota]] para enlazar conceptos.&#10;Usa #etiqueta para categorizar."
          />
        </div>

        <!-- Preview Pane -->
        <div
          v-show="viewMode === 'preview' || viewMode === 'split'"
          class="pane-wrapper preview-wrapper"
          @click="handlePreviewClick"
          v-html="renderedMarkdown"
        />
      </div>

      <!-- Backlinks Panel if note exists -->
      <div v-if="note && note.backlinks" class="modal-footer-backlinks">
        <BacklinksPanel
          :backlinks="note.backlinks"
          @navigate="(b) => emit('openWikilink', b.title)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  padding: 20px;
}

.note-modal-card {
  width: 100%;
  max-width: 900px;
  height: 85vh;
  display: flex;
  flex-direction: column;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.note-type-icon {
  font-size: 1.4rem;
}

.note-title-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--hermes-text-primary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mode-switcher {
  display: flex;
  background: rgba(0, 0, 0, 0.3);
  padding: 3px;
  border-radius: 6px;
}

.mode-btn {
  background: none;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--hermes-text-muted);
  cursor: pointer;
}

.mode-btn.is-active {
  background: rgba(255, 255, 255, 0.12);
  color: var(--hermes-text-primary);
}

.save-btn {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted);
  font-size: 1.3rem;
  cursor: pointer;
}

.tags-input-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.tags-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--hermes-text-muted);
}

.tags-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: var(--hermes-accent-blue, #00E5FF);
  font-size: 0.8rem;
}

.workspace-body {
  flex: 1;
  display: grid;
  gap: 14px;
  margin-top: 12px;
  min-height: 0;
  overflow: hidden;
}

.workspace-body.mode-split {
  grid-template-columns: 1fr 1fr;
}

.workspace-body.mode-edit {
  grid-template-columns: 1fr;
}

.workspace-body.mode-preview {
  grid-template-columns: 1fr;
}

.pane-wrapper {
  height: 100%;
  display: flex;
  overflow: hidden;
}

.editor-textarea {
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 14px;
  color: var(--hermes-text-primary);
  font-family: 'Fira Code', monospace, sans-serif;
  font-size: 0.85rem;
  line-height: 1.6;
  outline: none;
  resize: none;
}

.editor-textarea:focus {
  border-color: rgba(0, 229, 255, 0.4);
}

.preview-wrapper {
  height: 100%;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 16px;
  color: var(--hermes-text-primary);
  font-size: 0.88rem;
  line-height: 1.6;
}

:deep(.wikilink-btn) {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  background: rgba(0, 229, 255, 0.15);
  border: 1px solid rgba(0, 229, 255, 0.35);
  color: var(--hermes-accent-blue, #00E5FF);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

:deep(.wikilink-btn:hover) {
  background: rgba(0, 229, 255, 0.3);
  box-shadow: 0 0 8px rgba(0, 229, 255, 0.4);
}

:deep(.preview-tag) {
  color: var(--hermes-accent-pink, #FF007F);
  font-weight: 700;
}

.modal-footer-backlinks {
  margin-top: 12px;
  max-height: 120px;
  overflow-y: auto;
}
</style>

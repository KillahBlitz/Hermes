<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ZettelNote, KnowledgeGraphData, BacklinkItem } from '~/composables/useProgress'
import ZettelkastenTagPill from '~/components/atoms/ZettelkastenTagPill.vue'
import BacklinksPanel from '~/components/molecules/BacklinksPanel.vue'
import KnowledgeGraphView from '~/components/organisms/KnowledgeGraphView.vue'

const props = defineProps<{
  notes: ZettelNote[]
  activeNote: ZettelNote | null
  search: string
  selectedTag: string
  isGraphView: boolean
  graphData: KnowledgeGraphData
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'update:search', val: string): void
  (e: 'update:selectedTag', val: string): void
  (e: 'update:isGraphView', val: boolean): void
  (e: 'selectNote', note: ZettelNote): void
  (e: 'createNote'): void
  (e: 'saveNote', note: ZettelNote): void
  (e: 'deleteNote', note: ZettelNote): void
  (e: 'openWikilink', targetTitle: string): void
}>()

// Editor Mode: 'edit' | 'preview' | 'split'
const editorMode = ref<'edit' | 'preview' | 'split'>('split')
const editedTitle = ref('')
const editedContent = ref('')

watch(() => props.activeNote, (note) => {
  if (note) {
    editedTitle.value = note.title
    editedContent.value = note.content_md
  }
}, { immediate: true })

const handleSave = () => {
  if (!props.activeNote) return
  emit('saveNote', {
    ...props.activeNote,
    title: editedTitle.value.trim() || props.activeNote.title,
    content_md: editedContent.value
  })
}

// Convert markdown with [[wikilinks]] into HTML preview
const renderedMarkdown = computed(() => {
  if (!editedContent.value) return '<p class="empty-preview">Sin contenido escrito aún...</p>'
  
  let html = editedContent.value
    // Escape basic HTML
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    // Headers
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    // Bold & Italic
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    // Code blocks
    .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>')
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    // Lists
    .replace(/^\- (.*$)/gim, '<li>$1</li>')
    // Paragraphs
    .replace(/\n\n/gim, '</p><p>')

  // Replace [[wikilinks]] with clickable spans
  html = html.replace(/\[\[(.*?)\]\]/g, (match, p1) => {
    return `<button type="button" class="wikilink-btn" data-wikilink="${p1.trim()}">🔗 ${p1.trim()}</button>`
  })

  // Replace #tags
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
</script>

<template>
  <div class="zettelkasten-vault-view">
    <!-- Top Bar: Stats & View Toggle -->
    <div class="vault-topbar glass-panel">
      <div class="topbar-left">
        <span class="vault-badge text-accent-blue">🧠 Bóveda Zettelkasten</span>
        <span class="vault-stats">{{ notes.length }} notas indexadas</span>
      </div>

      <div class="view-toggle">
        <button
          type="button"
          class="toggle-btn"
          :class="{ 'is-active': !isGraphView }"
          @click="emit('update:isGraphView', false)"
        >
          <span>📝 Notas & Editor</span>
        </button>
        <button
          type="button"
          class="toggle-btn"
          :class="{ 'is-active': isGraphView }"
          @click="emit('update:isGraphView', true)"
        >
          <span>🌐 Grafo 2D</span>
        </button>
      </div>
    </div>

    <!-- 1. GRAPH VIEW -->
    <div v-if="isGraphView" class="graph-container">
      <KnowledgeGraphView
        :graph-data="graphData"
        @select-node="(title) => { emit('openWikilink', title); emit('update:isGraphView', false); }"
      />
    </div>

    <!-- 2. NOTES & EDITOR VIEW -->
    <div v-else class="vault-split-layout">
      <!-- Left Sidebar: Search & Notes List -->
      <div class="notes-sidebar glass-panel">
        <div class="sidebar-header">
          <div class="search-box">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              type="text"
              class="search-input"
              placeholder="Buscar notas o contenido..."
              :value="search"
              @input="emit('update:search', ($event.target as HTMLInputElement).value)"
            >
          </div>

          <button
            type="button"
            class="new-note-btn btn-neon-blue"
            title="Crear nueva nota"
            @click="emit('createNote')"
          >
            <span>＋ Nota</span>
          </button>
        </div>

        <!-- Tag Filter Pills -->
        <div v-if="graphData.all_tags.length > 0" class="tags-row">
          <ZettelkastenTagPill
            tag="todas"
            :active="selectedTag === ''"
            @click="emit('update:selectedTag', '')"
          />
          <ZettelkastenTagPill
            v-for="t in graphData.all_tags"
            :key="t"
            :tag="t"
            :active="selectedTag === t"
            @click="emit('update:selectedTag', t)"
          />
        </div>

        <!-- Notes List -->
        <div class="notes-list">
          <div
            v-for="note in notes"
            :key="note.id"
            class="note-list-item"
            :class="{ 'is-active': activeNote?.id === note.id }"
            @click="emit('selectNote', note)"
          >
            <div class="note-item-header">
              <span class="note-item-title">{{ note.title }}</span>
              <span v-if="note.backlinks?.length" class="backlink-pill" title="Backlinks recibidos">
                🔗 {{ note.backlinks.length }}
              </span>
            </div>

            <div v-if="note.tags?.length" class="note-item-tags">
              <span v-for="tag in note.tags.slice(0, 3)" :key="tag" class="micro-tag">
                #{{ tag }}
              </span>
            </div>
          </div>

          <div v-if="notes.length === 0" class="notes-empty">
            <p>No se encontraron notas con estos filtros.</p>
          </div>
        </div>
      </div>

      <!-- Right Main: Markdown Editor & Backlinks -->
      <div v-if="activeNote" class="editor-main glass-panel">
        <!-- Editor Header -->
        <div class="editor-header">
          <div class="title-edit-wrapper">
            <input
              v-model="editedTitle"
              type="text"
              class="title-input"
              placeholder="Título de la nota..."
            >
          </div>

          <div class="editor-actions">
            <!-- Mode Switcher -->
            <div class="mode-switcher">
              <button
                type="button"
                class="mode-btn"
                :class="{ 'is-active': editorMode === 'edit' }"
                @click="editorMode = 'edit'"
              >
                Editor
              </button>
              <button
                type="button"
                class="mode-btn"
                :class="{ 'is-active': editorMode === 'split' }"
                @click="editorMode = 'split'"
              >
                Dividido
              </button>
              <button
                type="button"
                class="mode-btn"
                :class="{ 'is-active': editorMode === 'preview' }"
                @click="editorMode = 'preview'"
              >
                Vista previa
              </button>
            </div>

            <button
              type="button"
              class="btn-neon-teal save-btn"
              @click="handleSave"
            >
              Guardar
            </button>

            <button
              type="button"
              class="delete-note-btn"
              title="Eliminar nota"
              @click="emit('deleteNote', activeNote)"
            >
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6" />
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Editor Content Area -->
        <div class="editor-workspace" :class="`mode-${editorMode}`">
          <!-- Textarea Editor -->
          <div v-show="editorMode === 'edit' || editorMode === 'split'" class="textarea-pane">
            <textarea
              v-model="editedContent"
              class="markdown-textarea"
              placeholder="Escribe apuntes en Markdown... Usa [[Nombre De Nota]] para enlazar y #etiqueta para categorizar."
            />
          </div>

          <!-- Live Preview Pane -->
          <div
            v-show="editorMode === 'preview' || editorMode === 'split'"
            class="preview-pane"
            @click="handlePreviewClick"
            v-html="renderedMarkdown"
          />
        </div>

        <!-- Bottom Backlinks Section -->
        <div class="editor-bottom">
          <BacklinksPanel
            :backlinks="activeNote.backlinks || []"
            @navigate="(b) => emit('openWikilink', b.title)"
          />
        </div>
      </div>

      <!-- Empty State if no note selected -->
      <div v-else class="editor-empty glass-panel">
        <span class="empty-icon">🧠</span>
        <h3>Bóveda de Conocimiento Zettelkasten</h3>
        <p>Selecciona una nota del menú izquierdo o crea una nueva para documentar conceptos y entrelazar ideas con <code>[[wikilinks]]</code>.</p>
        <button
          type="button"
          class="btn-neon-blue"
          @click="emit('createNote')"
        >
          ＋ Crear Primera Nota
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.zettelkasten-vault-view {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.vault-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-radius: 12px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.vault-badge {
  font-size: 0.95rem;
  font-weight: 800;
}

.vault-stats {
  font-size: 0.78rem;
  color: var(--hermes-text-muted);
}

.text-accent-blue { color: var(--hermes-accent-blue, #00E5FF); }

.view-toggle {
  display: flex;
  background: rgba(0, 0, 0, 0.3);
  padding: 3px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.toggle-btn {
  padding: 5px 12px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: var(--hermes-text-muted);
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.toggle-btn.is-active {
  background: rgba(0, 229, 255, 0.18);
  color: var(--hermes-accent-blue, #00E5FF);
}

.vault-split-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 16px;
  min-height: calc(100vh - 280px);
}

@media (max-width: 900px) {
  .vault-split-layout {
    grid-template-columns: 1fr;
  }
}

.notes-sidebar {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border-radius: 14px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
  height: 100%;
}

.sidebar-header {
  display: flex;
  gap: 8px;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 6px 10px;
  border-radius: 8px;
  color: var(--hermes-text-muted);
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: var(--hermes-text-primary);
  font-size: 0.8rem;
}

.new-note-btn {
  padding: 6px 10px;
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: 8px;
  cursor: pointer;
}

.tags-row {
  display: flex;
  align-items: center;
  gap: 4px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.notes-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow-y: auto;
  max-height: 520px;
}

.note-list-item {
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  cursor: pointer;
  transition: all 0.2s ease;
}

.note-list-item:hover {
  background: rgba(0, 229, 255, 0.08);
  border-color: rgba(0, 229, 255, 0.25);
}

.note-list-item.is-active {
  background: rgba(0, 229, 255, 0.15);
  border-color: var(--hermes-accent-blue, #00E5FF);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
}

.note-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.note-item-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.backlink-pill {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--hermes-accent-pink, #FF007F);
  background: rgba(255, 0, 127, 0.12);
  padding: 1px 6px;
  border-radius: 999px;
}

.note-item-tags {
  display: flex;
  gap: 4px;
  margin-top: 4px;
}

.micro-tag {
  font-size: 0.7rem;
  color: var(--hermes-text-muted);
}

.notes-empty {
  text-align: center;
  padding: 30px 10px;
  color: var(--hermes-text-muted);
  font-size: 0.82rem;
}

.editor-main {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 20px;
  border-radius: 14px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.title-edit-wrapper {
  flex: 1;
  min-width: 200px;
}

.title-input {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--hermes-text-primary);
}

.editor-actions {
  display: flex;
  align-items: center;
  gap: 8px;
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
  padding: 5px 12px;
  font-size: 0.78rem;
  font-weight: 700;
  border-radius: 6px;
  cursor: pointer;
}

.delete-note-btn {
  background: rgba(255, 77, 77, 0.08);
  border: 1px solid rgba(255, 77, 77, 0.2);
  color: #ff4d4d;
  padding: 5px 8px;
  border-radius: 6px;
  cursor: pointer;
}

.delete-note-btn:hover {
  background: rgba(255, 77, 77, 0.2);
}

.editor-workspace {
  display: grid;
  gap: 16px;
  min-height: 380px;
}

.editor-workspace.mode-split {
  grid-template-columns: 1fr 1fr;
}

.editor-workspace.mode-edit {
  grid-template-columns: 1fr;
}

.editor-workspace.mode-preview {
  grid-template-columns: 1fr;
}

.textarea-pane {
  display: flex;
  height: 100%;
}

.markdown-textarea {
  width: 100%;
  height: 380px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 14px;
  color: var(--hermes-text-primary);
  font-family: 'Fira Code', monospace, sans-serif;
  font-size: 0.85rem;
  line-height: 1.6;
  outline: none;
  resize: vertical;
}

.markdown-textarea:focus {
  border-color: rgba(0, 229, 255, 0.4);
}

.preview-pane {
  height: 380px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 14px;
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

.editor-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  text-align: center;
  border-radius: 14px;
  gap: 12px;
}

.empty-icon {
  font-size: 3.2rem;
}

.editor-empty h3 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--hermes-text-primary);
}

.editor-empty p {
  margin: 0;
  max-width: 440px;
  font-size: 0.88rem;
  color: var(--hermes-text-muted);
  line-height: 1.5;
}

.editor-empty code {
  color: var(--hermes-accent-teal, #00FFC6);
}
</style>

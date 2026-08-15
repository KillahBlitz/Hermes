<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Category } from '~/composables/useFinance'
import CategoryTag from '~/components/atoms/CategoryTag.vue'

const props = defineProps<{
  show: boolean
  categories: Category[]
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'create', payload: { name: string; type: 'INCOME' | 'EXPENSE'; icon: string; color: string }): void
  (e: 'delete', categoryId: string): void
}>()

const activeTab = ref<'EXPENSE' | 'INCOME'>('EXPENSE')

const newName = ref('')
const newType = ref<'INCOME' | 'EXPENSE'>('EXPENSE')
const newIcon = ref('🏷️')
const newColor = ref('#00FFC6')

const EMOJI_PALETTE = [
  '🛒', '🏠', '🚗', '🍿', '💊', '📚', '🛍️', '⚙️',
  '💼', '💻', '📈', '🎁', '💰', '🍔', '✈️', '🎮',
  '🏋️', '☕', '👶', '🐾', '💳', '💡', '🏷️', '💎'
]

const COLOR_PALETTE = [
  '#00FFC6', '#00E5FF', '#FF007F', '#FFD166',
  '#06D6A0', '#118AB2', '#B5179E', '#7209B7',
  '#F72585', '#4CC9F0', '#FF5722', '#94949E'
]

const filteredCategories = computed(() => {
  return props.categories.filter((c) => c.type === activeTab.value)
})

const onCreateCategory = () => {
  if (!newName.value.trim()) return
  emit('create', {
    name: newName.value.trim(),
    type: newType.value,
    icon: newIcon.value,
    color: newColor.value
  })
  newName.value = ''
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <div class="modal-header">
        <div class="modal-title-group">
          <h3 class="modal-title">Gestor de Categorías</h3>
          <span class="modal-subtitle">Personaliza iconos, colores y nombres</span>
        </div>
        <button class="close-btn" @click="emit('close')">✕</button>
      </div>

      <!-- Pestañas de Gastos / Ingresos -->
      <div class="tabs-nav">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'EXPENSE' }"
          @click="activeTab = 'EXPENSE'"
        >
          Categorías de Gastos ({{ categories.filter(c => c.type === 'EXPENSE').length }})
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'INCOME' }"
          @click="activeTab = 'INCOME'"
        >
          Categorías de Ingresos ({{ categories.filter(c => c.type === 'INCOME').length }})
        </button>
      </div>

      <!-- Formulario Nueva Categoría -->
      <div class="new-category-box">
        <h4 class="box-title">Crear Nueva Categoría</h4>

        <div class="new-cat-form">
          <div class="type-toggle-mini">
            <button
              type="button"
              class="mini-btn"
              :class="{ active: newType === 'EXPENSE' }"
              @click="newType = 'EXPENSE'"
            >
              Gasto
            </button>
            <button
              type="button"
              class="mini-btn"
              :class="{ active: newType === 'INCOME' }"
              @click="newType = 'INCOME'"
            >
              Ingreso
            </button>
          </div>

          <div class="input-row">
            <!-- Icono seleccionado -->
            <div class="selected-icon-preview">
              <span class="icon-char">{{ newIcon }}</span>
            </div>

            <!-- Nombre -->
            <input
              v-model="newName"
              type="text"
              placeholder="Nombre de la categoría..."
              maxlength="50"
              class="cat-name-input"
              @keydown.enter.prevent="onCreateCategory"
            />

            <!-- Botón Crear -->
            <button
              class="add-cat-btn glow-teal"
              :disabled="!newName.trim() || loading"
              @click="onCreateCategory"
            >
              + Agregar
            </button>
          </div>

          <!-- Selector de Emojis -->
          <div class="palette-group">
            <span class="palette-label">Icono:</span>
            <div class="emojis-picker">
              <button
                v-for="em in EMOJI_PALETTE"
                :key="em"
                type="button"
                class="emoji-choice-btn"
                :class="{ active: newIcon === em }"
                @click="newIcon = em"
              >
                {{ em }}
              </button>
            </div>
          </div>

          <!-- Selector de Colores Neón -->
          <div class="palette-group">
            <span class="palette-label">Color Neón:</span>
            <div class="colors-picker">
              <button
                v-for="col in COLOR_PALETTE"
                :key="col"
                type="button"
                class="color-choice-btn"
                :class="{ active: newColor === col }"
                :style="{ backgroundColor: col, boxShadow: newColor === col ? `0 0 12px ${col}` : 'none' }"
                @click="newColor = col"
              ></button>
            </div>
          </div>
        </div>
      </div>

      <!-- Lista de Categorías Existentes -->
      <div class="categories-list-box">
        <h4 class="box-title">Categorías Existentes</h4>
        <div class="categories-grid">
          <div
            v-for="cat in filteredCategories"
            :key="cat.id"
            class="category-item-card"
          >
            <CategoryTag
              :name="cat.name"
              :icon="cat.icon"
              :color="cat.color"
              size="md"
            />

            <div class="cat-item-actions">
              <span v-if="cat.is_default" class="default-badge" title="Categoría base del sistema">Base</span>
              <button
                v-else
                class="delete-cat-btn"
                title="Eliminar categoría personalizada"
                @click="emit('delete', cat.id)"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  animation: fadeIn 0.15s ease-out;
}

.modal-card {
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 20px;
  padding: 24px;
  background: rgba(23, 23, 28, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
  animation: scaleUp 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 18px;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0 0 4px 0;
}

.modal-subtitle {
  font-size: 0.8rem;
  color: var(--hermes-text-muted, #94949E);
}

.close-btn {
  background: rgba(255, 255, 255, 0.05);
  border: none;
  color: var(--hermes-text-muted, #94949E);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}

/* Tabs */
.tabs-nav {
  display: flex;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 3px;
  margin-bottom: 20px;
}

.tab-btn {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--hermes-text-muted, #94949E);
  padding: 8px 12px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.82rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn.active {
  background: var(--hermes-bg-surface, #17171c);
  color: var(--hermes-text-primary, #F4F4F5);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

.box-title {
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--hermes-text-muted, #94949E);
  margin-bottom: 12px;
}

/* Formulario Nueva Categoría */
.new-category-box {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 20px;
}

.new-cat-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.type-toggle-mini {
  display: inline-flex;
  background: rgba(255, 255, 255, 0.04);
  padding: 2px;
  border-radius: 8px;
  width: fit-content;
}

.mini-btn {
  background: transparent;
  border: none;
  color: var(--hermes-text-muted, #94949E);
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
}

.mini-btn.active {
  background: rgba(255, 255, 255, 0.12);
  color: var(--hermes-text-primary, #F4F4F5);
}

.input-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.selected-icon-preview {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.cat-name-input {
  flex: 1;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 9px 14px;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.88rem;
  outline: none;
}

.cat-name-input:focus {
  border-color: var(--hermes-accent-teal, #00FFC6);
}

.add-cat-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  font-weight: 800;
  font-size: 0.82rem;
  padding: 9px 14px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-cat-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.palette-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.palette-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--hermes-text-muted, #94949E);
}

.emojis-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  max-height: 72px;
  overflow-y: auto;
}

.emoji-choice-btn {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid transparent;
  border-radius: 6px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.1s ease;
}

.emoji-choice-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.1);
}

.emoji-choice-btn.active {
  border-color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.15);
}

.colors-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.color-choice-btn {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.color-choice-btn:hover {
  transform: scale(1.2);
}

.color-choice-btn.active {
  border-color: #fff;
  transform: scale(1.25);
}

/* Lista */
.categories-list-box {
  display: flex;
  flex-direction: column;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 10px;
  max-height: 220px;
  overflow-y: auto;
  padding-right: 4px;
}

.category-item-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.cat-item-actions {
  display: flex;
  align-items: center;
}

.default-badge {
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--hermes-text-muted, #94949E);
  background: rgba(255, 255, 255, 0.06);
  padding: 2px 6px;
  border-radius: 4px;
}

.delete-cat-btn {
  background: rgba(255, 0, 127, 0.1);
  border: 1px solid rgba(255, 0, 127, 0.2);
  color: var(--hermes-accent-pink, #FF007F);
  width: 22px;
  height: 22px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  transition: all 0.15s ease;
}

.delete-cat-btn:hover {
  background: var(--hermes-accent-pink, #FF007F);
  color: #fff;
  box-shadow: 0 0 8px rgba(255, 0, 127, 0.4);
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
</style>

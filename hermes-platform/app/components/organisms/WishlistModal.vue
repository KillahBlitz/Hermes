<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { WishlistItem } from '~/composables/useLists'

const props = defineProps<{
  show: boolean
  itemToEdit?: WishlistItem | null
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: {
    id?: string
    name: string
    price: number
    currency?: string
    category?: string
    priority: string
    description?: string
    url?: string
    status?: string
  }): void
}>()

const formName = ref('')
const formPrice = ref<number | ''>('')
const formCurrency = ref('MXN')
const formCategory = ref('Tecnología')
const formPriority = ref<'ALTA' | 'MEDIA' | 'BAJA'>('MEDIA')
const formDescription = ref('')
const formUrl = ref('')
const formStatus = ref('PENDING')

const isEditing = computed(() => !!props.itemToEdit)

const CATEGORIES = [
  'Tecnología', 'Gaming', 'Hogar & Oficina', 'Ropa & Estilo',
  'Libros & Cursos', 'Herramientas', 'Salud & Deporte', 'Vehículos', 'General'
]

watch(
  () => props.show,
  (open) => {
    if (open) {
      if (props.itemToEdit) {
        formName.value = props.itemToEdit.name
        formPrice.value = props.itemToEdit.price
        formCurrency.value = props.itemToEdit.currency || 'MXN'
        formCategory.value = props.itemToEdit.category || 'General'
        formPriority.value = props.itemToEdit.priority
        formDescription.value = props.itemToEdit.description || ''
        formUrl.value = props.itemToEdit.url || ''
        formStatus.value = props.itemToEdit.status
      } else {
        formName.value = ''
        formPrice.value = ''
        formCurrency.value = 'MXN'
        formCategory.value = 'Tecnología'
        formPriority.value = 'MEDIA'
        formDescription.value = ''
        formUrl.value = ''
        formStatus.value = 'PENDING'
      }
    }
  }
)

const onSubmit = () => {
  if (!formName.value.trim() || formPrice.value === '') return
  emit('save', {
    id: props.itemToEdit?.id,
    name: formName.value.trim(),
    price: Number(formPrice.value),
    currency: formCurrency.value,
    category: formCategory.value,
    priority: formPriority.value,
    description: formDescription.value.trim() || undefined,
    url: formUrl.value.trim() || undefined,
    status: formStatus.value
  })
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <div class="modal-header">
        <div class="modal-title-group">
          <h3 class="modal-title">{{ isEditing ? 'Editar Deseo' : 'Nuevo Deseo de Compra' }}</h3>
          <span class="modal-subtitle">Registra compras futuras, gadgets o inversiones personales</span>
        </div>
        <button class="close-btn" @click="emit('close')">✕</button>
      </div>

      <form class="modal-form" @submit.prevent="onSubmit">
        <!-- Nombre del Artículo -->
        <div class="form-group">
          <label class="form-label">Nombre del Artículo *</label>
          <input
            v-model="formName"
            type="text"
            placeholder="ej. Monitor LG UltraWide 34'' Curvo"
            required
            maxlength="120"
            class="form-input"
          />
        </div>

        <!-- Precio y Moneda -->
        <div class="form-row">
          <div class="form-group flex-2">
            <label class="form-label">Precio Estimado *</label>
            <input
              v-model="formPrice"
              type="number"
              step="0.01"
              min="0"
              placeholder="0.00"
              required
              class="form-input"
            />
          </div>

          <div class="form-group flex-1">
            <label class="form-label">Moneda</label>
            <select v-model="formCurrency" class="form-select">
              <option value="MXN">MXN ($)</option>
              <option value="USD">USD ($)</option>
              <option value="EUR">EUR (€)</option>
            </select>
          </div>
        </div>

        <!-- Categoría y Prioridad -->
        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Categoría</label>
            <select v-model="formCategory" class="form-select">
              <option v-for="cat in CATEGORIES" :key="cat" :value="cat">
                {{ cat }}
              </option>
            </select>
          </div>

          <div class="form-group flex-1">
            <label class="form-label">Prioridad de Deseo</label>
            <select v-model="formPriority" class="form-select">
              <option value="ALTA">🔥 Alta (Urgente)</option>
              <option value="MEDIA">⚡ Media (Próxima)</option>
              <option value="BAJA">💤 Baja (Futura)</option>
            </select>
          </div>
        </div>

        <!-- Enlace de Compra -->
        <div class="form-group">
          <label class="form-label">Enlace de Compra Web (Tienda / Distribuidor)</label>
          <input
            v-model="formUrl"
            type="url"
            placeholder="https://www.amazon.com.mx/dp/..."
            maxlength="500"
            class="form-input"
          />
        </div>

        <!-- Descripción / Notas -->
        <div class="form-group">
          <label class="form-label">Descripción o Especificaciones</label>
          <textarea
            v-model="formDescription"
            rows="2"
            placeholder="Talla, color, modelo, notas o especificaciones..."
            maxlength="1000"
            class="form-textarea"
          ></textarea>
        </div>

        <!-- Estado de Compra (si está editando) -->
        <div v-if="isEditing" class="form-group">
          <label class="form-label">Estado del Artículo</label>
          <select v-model="formStatus" class="form-select">
            <option value="PENDING">Pendiente</option>
            <option value="PURCHASED">Comprado ✓</option>
            <option value="ARCHIVED">Descartado</option>
          </select>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button type="button" class="cancel-btn" @click="emit('close')">
            Cancelar
          </button>
          <button
            type="submit"
            class="submit-btn glow-teal"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ isEditing ? 'Guardar Cambios' : 'Registrar Deseo' }}
          </button>
        </div>
      </form>
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
  max-width: 520px;
  border-radius: 20px;
  padding: 24px;
  background: rgba(23, 23, 28, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-top: 3px solid var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
  animation: scaleUp 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 20px;
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

.form-group {
  margin-bottom: 14px;
}

.form-label {
  display: block;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--hermes-text-muted, #94949E);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 9px 12px;
  color: var(--hermes-text-primary, #F4F4F5);
  font-size: 0.9rem;
  outline: none;
  transition: all 0.2s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  border-color: var(--hermes-accent-teal, #00FFC6);
  background: rgba(0, 255, 198, 0.03);
  box-shadow: 0 0 12px rgba(0, 255, 198, 0.15);
}

.form-select option {
  background: #17171c;
  color: #F4F4F5;
}

.form-row {
  display: flex;
  gap: 12px;
}

.flex-1 { flex: 1; }
.flex-2 { flex: 2; }

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.cancel-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted, #94949E);
  padding: 9px 16px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  padding: 9px 20px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 0.9rem;
  cursor: pointer;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
</style>

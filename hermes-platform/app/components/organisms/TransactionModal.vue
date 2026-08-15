<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { Category, Transaction } from '~/composables/useFinance'

const props = defineProps<{
  show: boolean
  categories: Category[]
  transactionToEdit?: Transaction | null
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: {
    id?: string
    title: string
    amount: number
    type: 'INCOME' | 'EXPENSE'
    category_id: string
    date: string
    notes?: string
    payment_method?: string
  }): void
}>()

const formType = ref<'INCOME' | 'EXPENSE'>('EXPENSE')
const formTitle = ref('')
const formAmount = ref<number | ''>('')
const formCategoryId = ref('')
const formDate = ref('')
const formNotes = ref('')
const formPaymentMethod = ref('')

const isEditing = computed(() => !!props.transactionToEdit)

const availableCategories = computed(() => {
  return props.categories.filter((c) => c.type === formType.value)
})

watch(
  () => props.show,
  (open) => {
    if (open) {
      if (props.transactionToEdit) {
        formType.value = props.transactionToEdit.type
        formTitle.value = props.transactionToEdit.title
        formAmount.value = props.transactionToEdit.amount
        formCategoryId.value = props.transactionToEdit.category_id
        formNotes.value = props.transactionToEdit.notes || ''
        formPaymentMethod.value = props.transactionToEdit.payment_method || ''

        // Formato para input datetime-local: YYYY-MM-DDTHH:mm
        const d = new Date(props.transactionToEdit.date)
        formDate.value = d.toISOString().slice(0, 16)
      } else {
        // Valores por defecto
        formType.value = 'EXPENSE'
        formTitle.value = ''
        formAmount.value = ''
        formNotes.value = ''
        formPaymentMethod.value = ''

        const now = new Date()
        formDate.value = now.toISOString().slice(0, 16)

        // Seleccionar primera categoría disponible
        const defaultCat = availableCategories.value[0]
        formCategoryId.value = defaultCat ? defaultCat.id : ''
      }
    }
  }
)

// Al cambiar el tipo (Ingreso / Gasto), auto-seleccionar la primera categoría de ese tipo
watch(formType, () => {
  if (!isEditing.value) {
    const defaultCat = availableCategories.value[0]
    if (defaultCat) formCategoryId.value = defaultCat.id
  }
})

const onSubmit = () => {
  if (!formTitle.value.trim()) return
  if (!formAmount.value || Number(formAmount.value) <= 0) return
  if (!formCategoryId.value) return

  emit('save', {
    id: props.transactionToEdit?.id,
    title: formTitle.value.trim(),
    amount: Number(formAmount.value),
    type: formType.value,
    category_id: formCategoryId.value,
    date: new Date(formDate.value).toISOString(),
    notes: formNotes.value.trim() || undefined,
    payment_method: formPaymentMethod.value || undefined
  })
}
</script>

<template>
  <div v-if="show" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel" :class="formType.toLowerCase()">
      <div class="modal-header">
        <div class="modal-title-group">
          <h3 class="modal-title">{{ isEditing ? 'Editar Movimiento' : 'Nuevo Movimiento' }}</h3>
          <span class="modal-subtitle">Registra tus ingresos y gastos categorizados</span>
        </div>
        <button class="close-btn" @click="emit('close')">✕</button>
      </div>

      <form class="modal-form" @submit.prevent="onSubmit">
        <!-- Selector Tipo (Ingreso vs Gasto) -->
        <div class="type-selector-bar">
          <button
            type="button"
            class="type-choice-btn expense"
            :class="{ active: formType === 'EXPENSE' }"
            @click="formType = 'EXPENSE'"
          >
            💸 Gasto / Egreso
          </button>
          <button
            type="button"
            class="type-choice-btn income"
            :class="{ active: formType === 'INCOME' }"
            @click="formType = 'INCOME'"
          >
            💵 Ingreso / Ganancia
          </button>
        </div>

        <!-- Monto -->
        <div class="form-group amount-group">
          <label class="form-label">Monto ($ MXN) *</label>
          <div class="amount-input-wrapper">
            <span class="currency-symbol">$</span>
            <input
              v-model="formAmount"
              type="number"
              step="0.01"
              min="0.01"
              placeholder="0.00"
              required
              class="form-input amount-input"
            />
          </div>
        </div>

        <!-- Concepto / Título -->
        <div class="form-group">
          <label class="form-label">Concepto o Título *</label>
          <input
            v-model="formTitle"
            type="text"
            placeholder="ej. Compra semanal de despensa"
            required
            maxlength="120"
            class="form-input"
          />
        </div>

        <!-- Categoría y Fecha en 2 columnas -->
        <div class="form-row">
          <div class="form-group flex-1">
            <label class="form-label">Categoría *</label>
            <select v-model="formCategoryId" required class="form-select">
              <option value="" disabled>Selecciona una categoría</option>
              <option
                v-for="cat in availableCategories"
                :key="cat.id"
                :value="cat.id"
              >
                {{ cat.icon }} {{ cat.name }}
              </option>
            </select>
          </div>

          <div class="form-group flex-1">
            <label class="form-label">Fecha y Hora *</label>
            <input
              v-model="formDate"
              type="datetime-local"
              required
              class="form-input"
            />
          </div>
        </div>

        <!-- Método de Pago y Notas -->
        <div class="form-group">
          <label class="form-label">Método de Pago (Opcional)</label>
          <select v-model="formPaymentMethod" class="form-select">
            <option value="">No especificado</option>
            <option value="CREDIT_CARD">💳 Tarjeta de Crédito</option>
            <option value="DEBIT_CARD">💳 Tarjeta de Débito</option>
            <option value="TRANSFER">📱 Transferencia / SPEI</option>
            <option value="CASH">💵 Efectivo</option>
            <option value="OTHER">⚙️ Otro</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Notas o Detalles (Opcional)</label>
          <textarea
            v-model="formNotes"
            rows="2"
            placeholder="Detalles adicionales, número de ticket, comercio..."
            maxlength="500"
            class="form-textarea"
          ></textarea>
        </div>

        <!-- Footer Acciones -->
        <div class="modal-footer">
          <button type="button" class="cancel-btn" @click="emit('close')">
            Cancelar
          </button>
          <button
            type="submit"
            class="submit-btn"
            :class="formType === 'INCOME' ? 'glow-teal' : 'glow-pink'"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ isEditing ? 'Guardar Cambios' : 'Registrar Movimiento' }}
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
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
  animation: scaleUp 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.modal-card.income {
  border-top: 3px solid var(--hermes-accent-teal, #00FFC6);
}

.modal-card.expense {
  border-top: 3px solid var(--hermes-accent-pink, #FF007F);
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
  transition: all 0.15s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}

/* Selector Tipo */
.type-selector-bar {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 18px;
  background: rgba(255, 255, 255, 0.03);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.type-choice-btn {
  background: transparent;
  border: none;
  padding: 10px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.85rem;
  color: var(--hermes-text-muted, #94949E);
  cursor: pointer;
  transition: all 0.2s ease;
}

.type-choice-btn.expense.active {
  background: rgba(255, 0, 127, 0.15);
  color: var(--hermes-accent-pink, #FF007F);
  box-shadow: 0 0 12px rgba(255, 0, 127, 0.2);
}

.type-choice-btn.income.active {
  background: rgba(0, 255, 198, 0.15);
  color: var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 0 12px rgba(0, 255, 198, 0.2);
}

/* Campos de Formulario */
.form-group {
  margin-bottom: 16px;
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

.amount-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.currency-symbol {
  position: absolute;
  left: 14px;
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--hermes-text-muted, #94949E);
}

.amount-input {
  padding-left: 32px !important;
  font-size: 1.35rem !important;
  font-weight: 800 !important;
  font-family: 'JetBrains Mono', monospace;
  color: var(--hermes-text-primary, #F4F4F5) !important;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 10px 14px;
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

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.cancel-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted, #94949E);
  padding: 10px 18px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.submit-btn {
  border: none;
  color: #0c0c0e;
  padding: 10px 22px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 0.92rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn.glow-teal {
  background: var(--hermes-accent-teal, #00FFC6);
  box-shadow: 0 0 16px rgba(0, 255, 198, 0.35);
}

.submit-btn.glow-pink {
  background: var(--hermes-accent-pink, #FF007F);
  color: #fff;
  box-shadow: 0 0 16px rgba(255, 0, 127, 0.35);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  filter: brightness(1.1);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>

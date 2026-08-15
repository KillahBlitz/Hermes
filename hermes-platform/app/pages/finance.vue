<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { useFinance, type Transaction } from '~/composables/useFinance'
import MonthSelector from '~/components/molecules/MonthSelector.vue'
import FinanceKpiCard from '~/components/molecules/FinanceKpiCard.vue'
import InsightBanner from '~/components/molecules/InsightBanner.vue'
import FinanceTrendsChart from '~/components/organisms/FinanceTrendsChart.vue'
import BalanceDonutChart from '~/components/organisms/BalanceDonutChart.vue'
import CategoryDonutChart from '~/components/organisms/CategoryDonutChart.vue'
import TransactionListSection from '~/components/organisms/TransactionListSection.vue'
import TransactionModal from '~/components/organisms/TransactionModal.vue'
import CategoryManagerModal from '~/components/organisms/CategoryManagerModal.vue'
import DeleteConfirmModal from '~/components/organisms/DeleteConfirmModal.vue'

useHead({
  title: 'Administración Económica | Hermes',
  meta: [{ name: 'description', content: 'Control financiero inteligente, analítica mensual y balance de gastos e ingresos.' }]
})

const { isAuthenticated, isLoading: isAuthLoading } = useAuth()
const router = useRouter()

const {
  currentYear,
  currentMonth,
  transactions,
  categories,
  summary,
  expenseBreakdown,
  incomeBreakdown,
  monthlyTrends,
  filterType,
  filterCategoryId,
  searchQuery,
  page,
  totalPages,
  totalTransactions,
  loadingTransactions,
  loadingAnalytics,
  loadingCategories,
  error,
  hasNextPage,
  hasPrevPage,
  createCategory,
  deleteCategory,
  createTransaction,
  updateTransaction,
  deleteTransaction,
  setPeriod,
  nextMonth,
  prevMonth,
  setFilterType,
  setFilterCategory,
  setSearch,
  nextPage,
  prevPage,
  refreshAll
} = useFinance()

// Estado de Modales
const showTransactionModal = ref(false)
const transactionToEdit = ref<Transaction | null>(null)
const isSavingTx = ref(false)

const showCategoryModal = ref(false)
const isSavingCategory = ref(false)

const showDeleteTxModal = ref(false)
const transactionToDelete = ref<Transaction | null>(null)
const isDeletingTx = ref(false)

const savingsHealthText = computed(() => {
  const rate = summary.value?.totals.savings_rate_percent || 0
  if (rate >= 30) return 'Saludable 🟢'
  if (rate >= 15) return 'Moderado 🟡'
  if (rate > 0) return 'Bajo 🟠'
  return 'Déficit 🔴'
})

// Control de Acceso: Exclusivo para usuario logeado con Google
const checkAccess = () => {
  if (!isAuthLoading.value && !isAuthenticated.value) {
    router.push('/login')
  }
}

watch(isAuthenticated, (authed) => {
  if (!authed && !isAuthLoading.value) {
    router.push('/login')
  }
})

onMounted(async () => {
  checkAccess()
  if (isAuthenticated.value) {
    await refreshAll()
  }
})

// Handlers de Transacciones
const handleOpenNewTransaction = () => {
  transactionToEdit.value = null
  showTransactionModal.value = true
}

const handleOpenEditTransaction = (tx: Transaction) => {
  transactionToEdit.value = tx
  showTransactionModal.value = true
}

const handleSaveTransaction = async (payload: {
  id?: string
  title: string
  amount: number
  type: 'INCOME' | 'EXPENSE'
  category_id: string
  date: string
  notes?: string
  payment_method?: string
}) => {
  isSavingTx.value = true
  try {
    if (payload.id) {
      await updateTransaction(payload.id, payload)
    } else {
      await createTransaction(payload)
    }
    showTransactionModal.value = false
  } catch (err: any) {
    alert(err?.message || 'Error al guardar la transacción')
  } finally {
    isSavingTx.value = false
  }
}

const handleOpenDeleteTransaction = (tx: Transaction) => {
  transactionToDelete.value = tx
  showDeleteTxModal.value = true
}

const handleConfirmDeleteTransaction = async () => {
  if (!transactionToDelete.value) return
  isDeletingTx.value = true
  try {
    await deleteTransaction(transactionToDelete.value.id)
    showDeleteTxModal.value = false
    transactionToDelete.value = null
  } catch (err: any) {
    alert(err?.message || 'Error al eliminar la transacción')
  } finally {
    isDeletingTx.value = false
  }
}

// Handlers de Categorías
const handleCreateCategory = async (payload: {
  name: string
  type: 'INCOME' | 'EXPENSE'
  icon: string
  color: string
}) => {
  isSavingCategory.value = true
  try {
    await createCategory(payload)
  } catch (err: any) {
    alert(err?.message || 'Error al crear la categoría')
  } finally {
    isSavingCategory.value = false
  }
}

const handleDeleteCategory = async (categoryId: string) => {
  if (!confirm('¿Deseas eliminar esta categoría personalizada? Las transacciones asociadas se reasignarán a "Otros".')) return
  try {
    await deleteCategory(categoryId)
  } catch (err: any) {
    alert(err?.message || 'Error al eliminar la categoría')
  }
}
</script>

<template>
  <div class="finance-page-container">
    <!-- Header Principal -->
    <div class="finance-header">
      <div class="header-titles">
        <h1 class="page-title">
          <span class="title-icon-wrapper">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="1" x2="12" y2="23"></line>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
          </span>
          Administración Económica
        </h1>
        <p class="page-subtitle">
          Control financiero privado y analítica mensual de ingresos, gastos y saldo a favor.
        </p>
      </div>

      <!-- Selector de Periodo y Acción Rápida -->
      <div class="header-actions">
        <MonthSelector
          :year="currentYear"
          :month="currentMonth"
          :loading="loadingAnalytics"
          @change="setPeriod"
          @prev="prevMonth"
          @next="nextMonth"
        />

        <button class="primary-btn glow-teal" @click="handleOpenNewTransaction">
          <span>+</span> Nuevo Movimiento
        </button>
      </div>
    </div>

    <!-- Alerta de Error si aplica -->
    <div v-if="error" class="alert-banner glass-panel">
      <span class="alert-icon">⚠️</span>
      <span class="alert-text">{{ error }}</span>
      <button class="retry-btn" @click="refreshAll">Reintentar</button>
    </div>

    <!-- KPIs Cuadrícula de 4 Tarjetas -->
    <div class="kpis-grid">
      <FinanceKpiCard
        title="Total Ingresos"
        :amount="summary?.totals.total_income || 0"
        type="INCOME"
        icon="💵"
        :mom-percentage="summary?.comparison_previous_month.income_percentage_change"
        :invert-sentiment="false"
        accent-color="#00FFC6"
      />

      <FinanceKpiCard
        title="Total Gastos"
        :amount="summary?.totals.total_expenses || 0"
        type="EXPENSE"
        icon="💸"
        :mom-percentage="summary?.comparison_previous_month.expense_percentage_change"
        :invert-sentiment="true"
        accent-color="#FF007F"
      />

      <FinanceKpiCard
        title="Balance Neto (Saldo a Favor)"
        :amount="summary?.totals.net_savings || 0"
        :type="(summary?.totals.net_savings || 0) >= 0 ? 'INCOME' : 'EXPENSE'"
        icon="⚖️"
        :mom-percentage="summary?.comparison_previous_month.savings_percentage_change"
        :invert-sentiment="false"
        accent-color="#00E5FF"
      />

      <FinanceKpiCard
        title="Tasa de Ahorro"
        :amount="summary?.totals.savings_rate_percent || 0"
        type="NEUTRAL"
        icon="🎯"
        :subtitle="`Estado: ${savingsHealthText}`"
        accent-color="#7209B7"
      />
    </div>

    <!-- Banner de Insights Inteligentes -->
    <InsightBanner
      :insights="summary?.top_insights"
      :month-name="summary?.period.month_name"
    />

    <!-- Sección Fila 1 de Gráficas: Tendencias Semestrales & Donut de Balance de Ejecución -->
    <div class="charts-row">
      <div class="chart-col trends-col">
        <FinanceTrendsChart
          :trends="monthlyTrends"
          :loading="loadingAnalytics"
        />
      </div>

      <div class="chart-col balance-col">
        <BalanceDonutChart
          :totals="summary?.totals"
          :loading="loadingAnalytics"
        />
      </div>
    </div>

    <!-- Sección Fila 2 de Gráficas: 2 Donuts de Desglose por Categoría (Gastos e Ingresos) -->
    <div class="category-donuts-row">
      <div class="category-donut-col">
        <CategoryDonutChart
          :breakdown="expenseBreakdown"
          breakdown-type="EXPENSE"
          title="Distribución de Gastos"
          subtitle="Porcentajes por Categoría de Egreso"
          :loading="loadingAnalytics"
        />
      </div>

      <div class="category-donut-col">
        <CategoryDonutChart
          :breakdown="incomeBreakdown"
          breakdown-type="INCOME"
          title="Distribución de Ingresos"
          subtitle="Porcentajes por Categoría de Entrada"
          :loading="loadingAnalytics"
        />
      </div>
    </div>

    <!-- Sección de Tabla y Movimientos -->
    <TransactionListSection
      :transactions="transactions"
      :categories="categories"
      :filter-type="filterType"
      :filter-category-id="filterCategoryId"
      :search-query="searchQuery"
      :page="page"
      :total-pages="totalPages"
      :total-transactions="totalTransactions"
      :has-next-page="hasNextPage"
      :has-prev-page="hasPrevPage"
      :loading="loadingTransactions"
      @change-filter-type="setFilterType"
      @change-filter-category="setFilterCategory"
      @search="setSearch"
      @next-page="nextPage"
      @prev-page="prevPage"
      @new-transaction="handleOpenNewTransaction"
      @open-category-manager="showCategoryModal = true"
      @edit-transaction="handleOpenEditTransaction"
      @delete-transaction="handleOpenDeleteTransaction"
    />

    <!-- Modal de Transacción (Crear / Editar) -->
    <TransactionModal
      :show="showTransactionModal"
      :categories="categories"
      :transaction-to-edit="transactionToEdit"
      :loading="isSavingTx"
      @close="showTransactionModal = false"
      @save="handleSaveTransaction"
    />

    <!-- Modal Gestor de Categorías -->
    <CategoryManagerModal
      :show="showCategoryModal"
      :categories="categories"
      :loading="isSavingCategory"
      @close="showCategoryModal = false"
      @create="handleCreateCategory"
      @delete="handleDeleteCategory"
    />

    <!-- Modal Confirmar Eliminación -->
    <DeleteConfirmModal
      :is-open="showDeleteTxModal"
      title="Eliminar movimiento"
      message="¿Estás seguro de que deseas eliminar permanentemente este movimiento?"
      :item-title="transactionToDelete ? `${transactionToDelete.title} ($${transactionToDelete.amount.toFixed(2)})` : ''"
      :is-deleting="isDeletingTx"
      @confirm="handleConfirmDeleteTransaction"
      @cancel="showDeleteTxModal = false"
    />
  </div>
</template>

<style scoped>
.finance-page-container {
  max-width: 1280px;
  margin: 0 auto;
  padding-bottom: 60px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Header */
.finance-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  padding-bottom: 8px;
}

.header-titles {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.65rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
  letter-spacing: -0.02em;
}

.title-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(0, 255, 198, 0.12);
  color: var(--hermes-accent-teal, #00FFC6);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 16px rgba(0, 255, 198, 0.2);
}

.page-subtitle {
  color: var(--hermes-text-muted, #94949E);
  font-size: 0.92rem;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.primary-btn {
  background: var(--hermes-accent-teal, #00FFC6);
  color: #0c0c0e;
  border: none;
  font-weight: 800;
  font-size: 0.9rem;
  padding: 10px 18px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 20px rgba(0, 255, 198, 0.4);
}

/* Alerta */
.alert-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 18px;
  border-radius: 12px;
  background: rgba(255, 0, 127, 0.08);
  border: 1px solid rgba(255, 0, 127, 0.25);
  color: var(--hermes-text-primary, #F4F4F5);
}

.alert-icon { font-size: 1.2rem; }

.alert-text {
  flex: 1;
  font-size: 0.88rem;
}

.retry-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #fff;
  padding: 4px 12px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.8rem;
  cursor: pointer;
}

/* Cuadrícula de KPIs */
.kpis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 18px;
}

/* Fila 1 de Gráficas: Tendencias & Donut de Balance */
.charts-row {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 20px;
}

.chart-col {
  min-height: 330px;
}

/* Fila 2 de Gráficas: 2 Donuts de Categorías (Gastos e Ingresos) */
.category-donuts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.category-donut-col {
  min-height: 330px;
}

@media (max-width: 992px) {
  .charts-row,
  .category-donuts-row {
    grid-template-columns: 1fr;
  }
}
</style>

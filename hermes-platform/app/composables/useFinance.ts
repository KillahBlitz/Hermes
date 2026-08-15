import { ref, computed } from 'vue'
import { useAuth } from '~/composables/useAuth'

export interface Category {
  id: string
  user_id?: string
  name: string
  type: 'INCOME' | 'EXPENSE'
  icon: string
  color: string
  is_default: boolean
  created_at?: string
}

export interface Transaction {
  id: string
  user_id: string
  title: string
  amount: number
  type: 'INCOME' | 'EXPENSE'
  category_id: string
  category?: Category
  date: string
  notes?: string
  payment_method?: string
  tags: string[]
  created_at: string
  updated_at: string
}

export interface PeriodInfo {
  year: number
  month: number
  month_name: string
}

export interface TotalsInfo {
  total_income: number
  total_expenses: number
  net_savings: number
  savings_rate_percent: number
}

export interface MomComparison {
  income_difference: number
  income_percentage_change?: number | null
  expense_difference: number
  expense_percentage_change?: number | null
  savings_difference: number
  savings_percentage_change?: number | null
}

export interface HighestExpenseInsight {
  id: string
  title: string
  amount: number
  category_name: string
  date: string
}

export interface HighestCategoryInsight {
  category_id: string
  category_name: string
  icon: string
  color: string
  total_amount: number
  percentage_of_total_expenses: number
}

export interface TopInsights {
  highest_single_expense?: HighestExpenseInsight | null
  highest_expense_category?: HighestCategoryInsight | null
}

export interface FinanceSummary {
  period: PeriodInfo
  totals: TotalsInfo
  comparison_previous_month: MomComparison
  top_insights: TopInsights
}

export interface CategoryBreakdownItem {
  category_id: string
  name: string
  icon: string
  color: string
  total: number
  percentage: number
  transaction_count: number
}

export interface CategoryBreakdown {
  year: number
  month: number
  type: string
  total: number
  breakdown: CategoryBreakdownItem[]
}

export interface MonthTrendItem {
  year: number
  month: number
  label: string
  income: number
  expenses: number
  savings: number
}

export interface MonthlyTrends {
  months: MonthTrendItem[]
}

export const useFinance = () => {
  const { sessionToken } = useAuth()
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBaseUrl

  const now = new Date()
  const currentYear = ref(now.getFullYear())
  const currentMonth = ref(now.getMonth() + 1)

  const transactions = ref<Transaction[]>([])
  const categories = ref<Category[]>([])
  const summary = ref<FinanceSummary | null>(null)
  const categoryBreakdown = ref<CategoryBreakdown | null>(null)
  const expenseBreakdown = ref<CategoryBreakdown | null>(null)
  const incomeBreakdown = ref<CategoryBreakdown | null>(null)
  const monthlyTrends = ref<MonthlyTrends | null>(null)

  const breakdownType = ref<'EXPENSE' | 'INCOME'>('EXPENSE')
  const filterType = ref<'all' | 'INCOME' | 'EXPENSE'>('all')
  const filterCategoryId = ref<string>('')
  const searchQuery = ref<string>('')

  const page = ref(1)
  const limit = ref(10)
  const totalTransactions = ref(0)
  const totalPages = ref(1)

  const loadingTransactions = ref(false)
  const loadingAnalytics = ref(false)
  const loadingCategories = ref(false)
  const error = ref<string | null>(null)

  const hasNextPage = computed(() => page.value < totalPages.value)
  const hasPrevPage = computed(() => page.value > 1)

  const getHeaders = () => {
    return {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${sessionToken.value || ''}`
    }
  }

  // ─────────────────────────────────────────────────────────────
  // CATEGORÍAS
  // ─────────────────────────────────────────────────────────────

  const fetchCategories = async (type?: 'INCOME' | 'EXPENSE') => {
    loadingCategories.value = true
    error.value = null
    try {
      const headers = await getHeaders()
      let url = `${apiBase}/api/v1/finance/categories`
      if (type) url += `?type=${type}`
      const res = await $fetch<{ categories: Category[]; total: number }>(url, { headers })
      categories.value = res.categories
    } catch (err: any) {
      loggerError('Error al cargar categorías', err)
      error.value = err?.data?.detail || 'No se pudieron cargar las categorías.'
    } finally {
      loadingCategories.value = false
    }
  }

  const createCategory = async (payload: { name: string; type: 'INCOME' | 'EXPENSE'; icon: string; color: string }) => {
    try {
      const headers = await getHeaders()
      const created = await $fetch<Category>(`${apiBase}/api/v1/finance/categories`, {
        method: 'POST',
        headers,
        body: payload
      })
      await fetchCategories()
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al crear categoría')
    }
  }

  const updateCategory = async (id: string, payload: Partial<Category>) => {
    try {
      const headers = await getHeaders()
      const updated = await $fetch<Category>(`${apiBase}/api/v1/finance/categories/${id}`, {
        method: 'PUT',
        headers,
        body: payload
      })
      await fetchCategories()
      await fetchTransactions()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar categoría')
    }
  }

  const deleteCategory = async (id: string) => {
    try {
      const headers = await getHeaders()
      await $fetch(`${apiBase}/api/v1/finance/categories/${id}`, {
        method: 'DELETE',
        headers
      })
      await fetchCategories()
      await refreshAll()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar categoría')
    }
  }

  // ─────────────────────────────────────────────────────────────
  // TRANSACCIONES
  // ─────────────────────────────────────────────────────────────

  const fetchTransactions = async () => {
    loadingTransactions.value = true
    error.value = null
    try {
      const headers = await getHeaders()
      const params = new URLSearchParams()
      params.append('year', currentYear.value.toString())
      params.append('month', currentMonth.value.toString())
      params.append('page', page.value.toString())
      params.append('limit', limit.value.toString())

      if (filterType.value !== 'all') params.append('type', filterType.value)
      if (filterCategoryId.value) params.append('category_id', filterCategoryId.value)
      if (searchQuery.value.trim()) params.append('search', searchQuery.value.trim())

      const res = await $fetch<{
        transactions: Transaction[]
        total: number
        page: number
        limit: number
        total_pages: number
      }>(`${apiBase}/api/v1/finance/transactions?${params.toString()}`, { headers })

      transactions.value = res.transactions
      totalTransactions.value = res.total
      totalPages.value = res.total_pages
      page.value = res.page
    } catch (err: any) {
      loggerError('Error al cargar transacciones', err)
      error.value = err?.data?.detail || 'No se pudieron cargar las transacciones.'
    } finally {
      loadingTransactions.value = false
    }
  }

  const createTransaction = async (data: {
    title: string
    amount: number
    type: 'INCOME' | 'EXPENSE'
    category_id: string
    date: string
    notes?: string
    payment_method?: string
    tags?: string[]
  }) => {
    try {
      const headers = await getHeaders()
      const created = await $fetch<Transaction>(`${apiBase}/api/v1/finance/transactions`, {
        method: 'POST',
        headers,
        body: data
      })
      await refreshAll()
      return created
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al registrar transacción')
    }
  }

  const updateTransaction = async (id: string, data: Partial<Transaction>) => {
    try {
      const headers = await getHeaders()
      const updated = await $fetch<Transaction>(`${apiBase}/api/v1/finance/transactions/${id}`, {
        method: 'PUT',
        headers,
        body: data
      })
      await refreshAll()
      return updated
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al actualizar transacción')
    }
  }

  const deleteTransaction = async (id: string) => {
    try {
      const headers = await getHeaders()
      await $fetch(`${apiBase}/api/v1/finance/transactions/${id}`, {
        method: 'DELETE',
        headers
      })
      await refreshAll()
    } catch (err: any) {
      throw new Error(err?.data?.detail || 'Error al eliminar transacción')
    }
  }

  // ─────────────────────────────────────────────────────────────
  // ANALÍTICA Y REPORTES
  // ─────────────────────────────────────────────────────────────

  const fetchAnalytics = async () => {
    loadingAnalytics.value = true
    try {
      const headers = getHeaders()
      const y = currentYear.value
      const m = currentMonth.value

      const [summaryRes, expenseRes, incomeRes, trendsRes] = await Promise.all([
        $fetch<FinanceSummary>(`${apiBase}/api/v1/finance/analytics/summary?year=${y}&month=${m}`, { headers }),
        $fetch<CategoryBreakdown>(`${apiBase}/api/v1/finance/analytics/category-breakdown?year=${y}&month=${m}&type=EXPENSE`, { headers }),
        $fetch<CategoryBreakdown>(`${apiBase}/api/v1/finance/analytics/category-breakdown?year=${y}&month=${m}&type=INCOME`, { headers }),
        $fetch<MonthlyTrends>(`${apiBase}/api/v1/finance/analytics/monthly-trends?year=${y}&month=${m}&count=6`, { headers })
      ])

      summary.value = summaryRes
      expenseBreakdown.value = expenseRes
      incomeBreakdown.value = incomeRes
      categoryBreakdown.value = breakdownType.value === 'EXPENSE' ? expenseRes : incomeRes
      monthlyTrends.value = trendsRes
    } catch (err: any) {
      loggerError('Error al cargar analítica financiera', err)
    } finally {
      loadingAnalytics.value = false
    }
  }

  const setPeriod = async (year: number, month: number) => {
    currentYear.value = year
    currentMonth.value = month
    page.value = 1
    transactions.value = []
    await refreshAll()
  }

  const nextMonth = async () => {
    let m = currentMonth.value + 1
    let y = currentYear.value
    if (m > 12) {
      m = 1
      y += 1
    }
    await setPeriod(y, m)
  }

  const prevMonth = async () => {
    let m = currentMonth.value - 1
    let y = currentYear.value
    if (m < 1) {
      m = 12
      y -= 1
    }
    await setPeriod(y, m)
  }

  const setFilterType = async (type: 'all' | 'INCOME' | 'EXPENSE') => {
    filterType.value = type
    page.value = 1
    transactions.value = []
    await fetchTransactions()
  }

  const setFilterCategory = async (catId: string) => {
    filterCategoryId.value = catId
    page.value = 1
    transactions.value = []
    await fetchTransactions()
  }

  const setSearch = async (q: string) => {
    searchQuery.value = q
    page.value = 1
    transactions.value = []
    await fetchTransactions()
  }

  const nextPage = async () => {
    if (hasNextPage.value) {
      page.value += 1
      await fetchTransactions()
    }
  }

  const prevPage = async () => {
    if (hasPrevPage.value) {
      page.value -= 1
      await fetchTransactions()
    }
  }

  const setBreakdownType = (type: 'EXPENSE' | 'INCOME') => {
    breakdownType.value = type
    categoryBreakdown.value = type === 'EXPENSE' ? expenseBreakdown.value : incomeBreakdown.value
  }

  const refreshAll = async () => {
    await Promise.all([
      fetchCategories(),
      fetchTransactions(),
      fetchAnalytics()
    ])
  }

  const loggerError = (msg: string, err: any) => {
    console.error(`[useFinance] ${msg}:`, err)
  }

  return {
    // Estado
    currentYear,
    currentMonth,
    transactions,
    categories,
    summary,
    categoryBreakdown,
    expenseBreakdown,
    incomeBreakdown,
    monthlyTrends,
    breakdownType,
    filterType,
    filterCategoryId,
    searchQuery,
    page,
    limit,
    totalTransactions,
    totalPages,
    loadingTransactions,
    loadingAnalytics,
    loadingCategories,
    error,
    hasNextPage,
    hasPrevPage,

    // Métodos
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory,
    fetchTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    fetchAnalytics,
    setPeriod,
    nextMonth,
    prevMonth,
    setFilterType,
    setFilterCategory,
    setSearch,
    nextPage,
    prevPage,
    setBreakdownType,
    refreshAll
  }
}

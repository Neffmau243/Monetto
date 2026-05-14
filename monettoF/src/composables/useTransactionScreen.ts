import { computed, onMounted, reactive, shallowRef, toValue, watch } from 'vue'
import type { MaybeRefOrGetter } from 'vue'
import { useAuthSession } from './useAuthSession'
import {
  createTransaction,
  deleteTransaction,
  getCategories,
  getDashboardSummary,
  getTransactions,
  updateTransaction,
} from '../services/monettoApi'
import {
  currentBudgetSnapshot,
  mapCategory,
  mapTransaction,
} from '../services/monettoMappers'
import type {
  BudgetSource,
  Category,
  PaginationState,
  Transaction,
  TransactionFiltersState,
  TransactionFormPayload,
  TransactionType,
} from '../types'
import { currentMonth, toNumber } from '../utils/formatters'

export function useTransactionScreen(transactionType: MaybeRefOrGetter<TransactionType>) {
  const { requireToken } = useAuthSession()
  const currentType = computed(() => toValue(transactionType))
  const isIncome = computed(() => currentType.value === 'INCOME')
  const title = computed(() => (isIncome.value ? 'Gestion de ingresos' : 'Gestion de gastos'))
  const ctaLabel = computed(() => (isIncome.value ? 'Anadir ingreso' : 'Anadir gasto'))
  const helper = computed(() =>
    isIncome.value
      ? 'Visualiza y administra tus flujos de capital entrante.'
      : 'Controla salidas, alertas de presupuesto y gastos recurrentes.',
  )

  const categories = shallowRef<Category[]>([])
  const transactions = shallowRef<Transaction[]>([])
  const editingTransaction = shallowRef<Transaction | null>(null)
  const budgetSnapshot = shallowRef(currentBudgetSnapshot())
  const budgetSource = shallowRef<BudgetSource | null>(null)
  const isLoading = shallowRef(false)
  const errorMessage = shallowRef('')
  const filters = reactive<TransactionFiltersState>({
    categoryId: '',
    dateFrom: '',
    dateTo: '',
  })
  const pagination = reactive<PaginationState>({
    total: 0,
    page: 1,
    limit: 10,
    totalPages: 1,
    hasNext: false,
    hasPrevious: false,
  })

  async function loadCategories() {
    const token = requireToken()
    const response = await getCategories(token, currentType.value)
    categories.value = response.map(mapCategory)
  }

  async function loadBudgetSnapshot() {
    if (isIncome.value) {
      budgetSnapshot.value = currentBudgetSnapshot()
      budgetSource.value = null
      return
    }

    const token = requireToken()
    const summary = await getDashboardSummary(token, currentMonth())
    budgetSource.value = summary.budget_info?.source ?? null
    budgetSnapshot.value = currentBudgetSnapshot(
      summary.budget_info?.amount,
      summary.budget_info?.spent,
      summary.budget_info?.remaining,
    )
  }

  async function loadTransactions(page = pagination.page) {
    const token = requireToken()
    const response = await getTransactions(token, {
      type: currentType.value,
      categoryId: filters.categoryId,
      dateFrom: filters.dateFrom,
      dateTo: filters.dateTo,
      page,
      limit: pagination.limit,
    })

    transactions.value = response.items.map(mapTransaction)
    pagination.total = response.total
    pagination.page = response.page
    pagination.limit = response.limit
    pagination.totalPages = response.total_pages
    pagination.hasNext = response.has_next
    pagination.hasPrevious = response.has_previous
  }

  async function loadScreen(page = 1) {
    isLoading.value = true
    errorMessage.value = ''

    try {
      await Promise.all([loadCategories(), loadBudgetSnapshot()])
      await loadTransactions(page)
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : 'No se pudo cargar la vista'
    } finally {
      isLoading.value = false
    }
  }

  async function saveTransaction(payload: TransactionFormPayload) {
    isLoading.value = true
    errorMessage.value = ''

    try {
      const token = requireToken()

      if (editingTransaction.value) {
        await updateTransaction(token, editingTransaction.value.id, payload)
      } else {
        await createTransaction(token, payload)
      }

      editingTransaction.value = null
      await loadScreen(1)
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : 'No se pudo guardar'
    } finally {
      isLoading.value = false
    }
  }

  async function removeTransaction(transactionId: number) {
    isLoading.value = true
    errorMessage.value = ''

    try {
      await deleteTransaction(requireToken(), transactionId)
      await loadTransactions(pagination.page)
      await loadBudgetSnapshot()
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : 'No se pudo eliminar'
    } finally {
      isLoading.value = false
    }
  }

  function applyFilters() {
    void loadTransactions(1)
  }

  function resetFilters() {
    filters.categoryId = ''
    filters.dateFrom = ''
    filters.dateTo = ''
    void loadTransactions(1)
  }

  function changePage(page: number) {
    void loadTransactions(page)
  }

  function startEdit(transaction: Transaction) {
    editingTransaction.value = transaction
  }

  function cancelEdit() {
    editingTransaction.value = null
  }

  watch(
    currentType,
    () => {
      filters.categoryId = ''
      filters.dateFrom = ''
      filters.dateTo = ''
      editingTransaction.value = null
      void loadScreen(1)
    },
    { flush: 'post' },
  )

  onMounted(() => {
    void loadScreen(1)
  })

  const visibleTransactions = computed(() => transactions.value)
  const total = computed(() =>
    visibleTransactions.value.reduce((sum, transaction) => sum + toNumber(transaction.amount), 0),
  )
  const categoryOptions = computed(() => categories.value)
  const budgetUsage = computed(() => {
    const limit = toNumber(budgetSnapshot.value.limit)

    return limit > 0 ? (toNumber(budgetSnapshot.value.spent) / limit) * 100 : 0
  })
  const hasBudgetLimit = computed(() => toNumber(budgetSnapshot.value.limit) > 0)
  const budgetModeLabel = computed(() =>
    budgetSource.value === 'DYNAMIC_INCOME'
      ? 'limite dinamico por ingresos'
      : 'presupuesto mensual',
  )

  return {
    applyFilters,
    budgetSnapshot,
    budgetUsage,
    budgetModeLabel,
    cancelEdit,
    categoryOptions,
    changePage,
    ctaLabel,
    editingTransaction,
    errorMessage,
    filters,
    helper,
    hasBudgetLimit,
    isIncome,
    isLoading,
    pagination,
    removeTransaction,
    resetFilters,
    saveTransaction,
    startEdit,
    title,
    total,
    visibleTransactions,
  }
}

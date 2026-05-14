import { computed, onMounted, shallowRef } from 'vue'
import { useAuthSession } from './useAuthSession'
import {
  getDashboardSummary,
  getExpensesByCategory,
  getMonthlyTrend,
  getTransactions,
} from '../services/monettoApi'
import {
  currentBudgetSnapshot,
  mapExpenseBreakdown,
  mapTransaction,
} from '../services/monettoMappers'
import type { DashboardSummaryOut, ExpensesByCategoryOut, MonthlyTrendOut, Transaction } from '../types'
import { currentMonth, formatMoney, formatMonthLabel, toNumber } from '../utils/formatters'

export interface DashboardStat {
  label: string
  value: string
  icon: string
  tone: 'neutral' | 'income' | 'expense' | 'success' | 'warning' | 'critical'
  detail: string
}

export interface DashboardTrendPoint {
  month: string
  monthLabel: string
  incomeHeight: number
  expenseHeight: number
  isCurrent: boolean
}

function balanceTone(balance: number, incomeTotal: number, budgetUsage: number) {
  if (balance < 0 || budgetUsage >= 100) {
    return 'critical'
  }

  if (balance === 0 || budgetUsage >= 85 || (incomeTotal > 0 && balance / incomeTotal < 0.15)) {
    return 'warning'
  }

  return 'success'
}

function balanceDetail(tone: ReturnType<typeof balanceTone>, month: string) {
  if (tone === 'critical') {
    return `Deficit o presupuesto agotado en ${month}`
  }

  if (tone === 'warning') {
    return `Margen ajustado en ${month}`
  }

  return `Margen saludable en ${month}`
}

export function useDashboardSummary() {
  const { requireToken } = useAuthSession()
  const selectedMonth = shallowRef(currentMonth())
  const summary = shallowRef<DashboardSummaryOut | null>(null)
  const expensesByCategory = shallowRef<ExpensesByCategoryOut[]>([])
  const trend = shallowRef<MonthlyTrendOut[]>([])
  const recentTransactionsRaw = shallowRef<Transaction[]>([])
  const isLoading = shallowRef(false)
  const errorMessage = shallowRef('')

  async function loadDashboard(month = selectedMonth.value) {
    isLoading.value = true
    errorMessage.value = ''

    try {
      const token = requireToken()
      const [summaryResponse, categoryResponse, trendResponse, transactionsResponse] =
        await Promise.all([
          getDashboardSummary(token, month),
          getExpensesByCategory(token, month),
          getMonthlyTrend(token, 6),
          getTransactions(token, { page: 1, limit: 5 }),
        ])

      summary.value = summaryResponse
      expensesByCategory.value = categoryResponse
      trend.value = trendResponse
      recentTransactionsRaw.value = transactionsResponse.items.map(mapTransaction)
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : 'No se pudo cargar el dashboard'
    } finally {
      isLoading.value = false
    }
  }

  onMounted(() => {
    void loadDashboard()
  })

  const incomeTotal = computed(() => toNumber(summary.value?.total_income ?? '0.00'))
  const expenseTotal = computed(() => toNumber(summary.value?.total_expenses ?? '0.00'))
  const balance = computed(() => toNumber(summary.value?.balance ?? '0.00'))
  const budgetSnapshot = computed(() =>
    currentBudgetSnapshot(
      summary.value?.budget_info?.amount,
      summary.value?.budget_info?.spent,
      summary.value?.budget_info?.remaining,
    ),
  )
  const budgetUsage = computed(() => toNumber(summary.value?.budget_info?.percentage ?? '0.00'))
  const budgetModeLabel = computed(() => {
    if (!summary.value?.budget_info) {
      return 'Sin limite activo'
    }

    return summary.value.budget_info.is_dynamic
      ? 'Limite dinamico por ingresos'
      : 'Presupuesto fijo mensual'
  })
  const budgetModeDetail = computed(() => {
    if (!summary.value?.budget_info) {
      return 'Registra ingresos o define un presupuesto fijo.'
    }

    return summary.value.budget_info.is_dynamic
      ? 'Se calcula con tus ingresos registrados del mes.'
      : 'Usa el presupuesto que guardaste para el mes.'
  })
  const categoryBreakdown = computed(() => expensesByCategory.value.map(mapExpenseBreakdown))
  const meaningfulTrend = computed(() => {
    const current = selectedMonth.value
    const rows = trend.value.filter(
      (point) =>
        point.month === current || toNumber(point.income) > 0 || toNumber(point.expenses) > 0,
    )

    return rows.length > 0 ? rows : trend.value.slice(-1)
  })
  const maxTrendValue = computed(() =>
    Math.max(
      1,
      ...meaningfulTrend.value.flatMap((point) => [toNumber(point.income), toNumber(point.expenses)]),
    ),
  )
  const trendPoints = computed<DashboardTrendPoint[]>(() =>
    meaningfulTrend.value.map((point) => ({
      month: point.month,
      monthLabel: formatMonthLabel(point.month),
      incomeHeight: Math.max((toNumber(point.income) / maxTrendValue.value) * 180, 6),
      expenseHeight: Math.max((toNumber(point.expenses) / maxTrendValue.value) * 180, 6),
      isCurrent: point.month === selectedMonth.value,
    })),
  )
  const recentTransactions = computed(() => recentTransactionsRaw.value)
  const currentBalanceTone = computed(() =>
    balanceTone(balance.value, incomeTotal.value, budgetUsage.value),
  )
  const stats = computed<DashboardStat[]>(() => [
    {
      label: 'Balance total',
      value: formatMoney(balance.value, 'auto'),
      icon: 'account_balance',
      tone: currentBalanceTone.value,
      detail: summary.value
        ? balanceDetail(currentBalanceTone.value, summary.value.month)
        : 'Esperando datos del backend',
    },
    {
      label: 'Ingresos del mes',
      value: formatMoney(incomeTotal.value),
      icon: 'trending_up',
      tone: 'income',
      detail: 'Total calculado por Monetto API',
    },
    {
      label: 'Gastos del mes',
      value: formatMoney(expenseTotal.value),
      icon: 'trending_down',
      tone: 'expense',
      detail: 'Total calculado por Monetto API',
    },
  ])

  return {
    balance,
    budgetModeDetail,
    budgetModeLabel,
    budgetSnapshot,
    budgetUsage,
    categoryBreakdown,
    errorMessage,
    expenseTotal,
    incomeTotal,
    isLoading,
    loadDashboard,
    recentTransactions,
    selectedMonth,
    stats,
    trendPoints,
  }
}

import { computed, shallowRef, watch } from 'vue'
import { useAuthSession } from './useAuthSession'
import { downloadMonthlyReportPdf, getMonthlyReportJson } from '../services/monettoApi'
import { mapExpenseBreakdown, mapTransaction } from '../services/monettoMappers'
import type { ReportMonthlyOut } from '../types'
import { currentMonth, toNumber } from '../utils/formatters'

export function useReportsSummary() {
  const { requireToken } = useAuthSession()
  const selectedPeriod = shallowRef(currentMonth())
  const report = shallowRef<ReportMonthlyOut | null>(null)
  const isLoading = shallowRef(false)
  const errorMessage = shallowRef('')

  async function loadReport() {
    isLoading.value = true
    errorMessage.value = ''

    try {
      report.value = await getMonthlyReportJson(requireToken(), selectedPeriod.value)
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : 'No se pudo cargar reporte'
    } finally {
      isLoading.value = false
    }
  }

  async function downloadPdf() {
    isLoading.value = true
    errorMessage.value = ''

    try {
      const blob = await downloadMonthlyReportPdf(requireToken(), selectedPeriod.value)
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `monetto-${selectedPeriod.value}.pdf`
      link.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : 'No se pudo descargar PDF'
    } finally {
      isLoading.value = false
    }
  }

  watch(selectedPeriod, loadReport, { immediate: true })

  const incomeTotal = computed(() => toNumber(report.value?.summary.total_income ?? '0.00'))
  const expenseTotal = computed(() => toNumber(report.value?.summary.total_expenses ?? '0.00'))
  const netResult = computed(() => toNumber(report.value?.summary.balance ?? '0.00'))
  const budgetModeLabel = computed(() => {
    if (!report.value?.summary.budget_info) {
      return 'Sin limite activo'
    }

    return report.value.summary.budget_info.is_dynamic
      ? 'Limite dinamico por ingresos'
      : 'Presupuesto fijo mensual'
  })
  const budgetRemaining = computed(() => report.value?.summary.budget_info?.remaining ?? '0.00')
  const budgetUsage = computed(() => toNumber(report.value?.summary.budget_info?.percentage ?? '0.00'))
  const savingRate = computed(() =>
    incomeTotal.value > 0 ? Math.round((netResult.value / incomeTotal.value) * 100) : 0,
  )
  const topExpenseCategories = computed(() =>
    (report.value?.expenses_by_category ?? []).map(mapExpenseBreakdown).slice(0, 4),
  )
  const previewTransactions = computed(() =>
    (report.value?.transactions ?? []).map(mapTransaction).slice(0, 10),
  )
  const previewJson = computed(() =>
    JSON.stringify(
      report.value ?? {
        month: selectedPeriod.value,
        summary: null,
        transactions: [],
      },
      null,
      2,
    ),
  )

  return {
    budgetModeLabel,
    budgetRemaining,
    budgetUsage,
    downloadPdf,
    errorMessage,
    expenseTotal,
    incomeTotal,
    isLoading,
    loadReport,
    netResult,
    previewJson,
    previewTransactions,
    savingRate,
    selectedPeriod,
    topExpenseCategories,
  }
}

<script setup lang="ts">
import ExpenseDistributionPanel from '../components/reports/ExpenseDistributionPanel.vue'
import ReportHero from '../components/reports/ReportHero.vue'
import ReportJsonPanel from '../components/reports/ReportJsonPanel.vue'
import ReportPeriodActions from '../components/reports/ReportPeriodActions.vue'
import ReportTransactionsTable from '../components/reports/ReportTransactionsTable.vue'
import SavingRatePanel from '../components/reports/SavingRatePanel.vue'
import { useReportsSummary } from '../composables/useReportsSummary'

const {
  budgetModeLabel,
  budgetRemaining,
  budgetUsage,
  downloadPdf,
  errorMessage,
  expenseTotal,
  incomeTotal,
  isLoading,
  netResult,
  previewJson,
  previewTransactions,
  savingRate,
  selectedPeriod,
  topExpenseCategories,
} = useReportsSummary()
</script>

<template>
  <section class="page-stack">
    <header class="page-header">
      <div>
        <h2>Reportes mensuales</h2>
        <p>Consulta resultados, distribución de gastos y detalle transaccional.</p>
      </div>
      <ReportPeriodActions v-model="selectedPeriod" @download="downloadPdf" />
    </header>

    <p v-if="errorMessage" class="page-error" role="alert">{{ errorMessage }}</p>
    <p v-else-if="isLoading" class="page-info">Cargando reporte desde Monetto API...</p>

    <div class="report-grid">
      <ReportHero :expense-total="expenseTotal" :income-total="incomeTotal" :net-result="netResult" />
      <SavingRatePanel
        :budget-mode-label="budgetModeLabel"
        :budget-remaining="budgetRemaining"
        :budget-usage="budgetUsage"
        :net-result="netResult"
        :saving-rate="savingRate"
      />
      <ExpenseDistributionPanel :categories="topExpenseCategories" />
      <ReportJsonPanel :preview-json="previewJson" />
    </div>

    <ReportTransactionsTable :transactions="previewTransactions" />
  </section>
</template>

<style scoped>
.page-stack {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}

.page-header h2 {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.25;
}

.page-header p {
  color: var(--text-muted);
}

.report-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr 1fr;
  gap: 24px;
}

.page-error,
.page-info {
  padding: 12px 14px;
  border-radius: var(--radius);
  font-weight: 800;
}

.page-error {
  border: 1px solid rgba(255, 109, 122, 0.28);
  background: var(--danger-soft);
  color: var(--danger);
}

.page-info {
  border: 1px solid rgba(8, 239, 245, 0.24);
  background: var(--primary-soft);
  color: var(--primary-strong);
}

@media (max-width: 1180px) {
  .report-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-header h2 {
    font-size: 28px;
  }

  .report-grid {
    grid-template-columns: 1fr;
  }
}
</style>

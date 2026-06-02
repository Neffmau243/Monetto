<script setup lang="ts">
import AppIcon from '../components/AppIcon.vue'
import BudgetSummaryPanel from '../components/dashboard/BudgetSummaryPanel.vue'
import CategoryBreakdownPanel from '../components/dashboard/CategoryBreakdownPanel.vue'
import DashboardStats from '../components/dashboard/DashboardStats.vue'
import MonthlyTrendPanel from '../components/dashboard/MonthlyTrendPanel.vue'
import RecentTransactionsPanel from '../components/dashboard/RecentTransactionsPanel.vue'
import { useDashboardSummary } from '../composables/useDashboardSummary'

const {
  budgetModeDetail,
  budgetModeLabel,
  budgetSnapshot,
  budgetUsage,
  categoryBreakdown,
  errorMessage,
  isLoading,
  loadDashboard,
  recentTransactions,
  stats,
  trendPoints,
} =
  useDashboardSummary()
</script>

<template>
  <section class="page-stack">
    <header class="page-header">
      <div>
        <h2>Panel de control</h2>
        <p>Bienvenido de nuevo, aquí tienes tu resumen financiero.</p>
      </div>
      <button class="secondary-action" type="button" :disabled="isLoading" @click="loadDashboard()">
        <AppIcon name="calendar_month" :size="20" />
        {{ isLoading ? 'Actualizando...' : 'Periodo actual' }}
      </button>
    </header>

    <p v-if="errorMessage" class="page-error" role="alert">{{ errorMessage }}</p>

    <DashboardStats :stats="stats" />

    <div class="dashboard-grid">
      <MonthlyTrendPanel :points="trendPoints" />
      <CategoryBreakdownPanel :categories="categoryBreakdown" />
      <BudgetSummaryPanel
        :limit="budgetSnapshot.limit"
        :mode-detail="budgetModeDetail"
        :mode-label="budgetModeLabel"
        :remaining="budgetSnapshot.remaining"
        :spent="budgetSnapshot.spent"
        :usage="budgetUsage"
      />
      <RecentTransactionsPanel :transactions="recentTransactions" />
    </div>
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

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

.page-error {
  padding: 12px 14px;
  border: 1px solid rgba(255, 109, 122, 0.28);
  border-radius: var(--radius);
  background: var(--danger-soft);
  color: var(--danger);
  font-weight: 800;
}

@media (max-width: 1180px) {
  .dashboard-grid {
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

  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>

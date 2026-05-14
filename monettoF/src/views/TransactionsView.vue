<script setup lang="ts">
import TransactionBudgetAlert from '../components/transactions/TransactionBudgetAlert.vue'
import TransactionFilters from '../components/transactions/TransactionFilters.vue'
import TransactionHeader from '../components/transactions/TransactionHeader.vue'
import TransactionQuickForm from '../components/transactions/TransactionQuickForm.vue'
import TransactionTable from '../components/transactions/TransactionTable.vue'
import { useTransactionScreen } from '../composables/useTransactionScreen'
import type { TransactionType } from '../types'

const props = defineProps<{
  transactionType: TransactionType
}>()

const {
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
} = useTransactionScreen(() => props.transactionType)
</script>

<template>
  <section class="page-stack">
    <TransactionHeader :cta-label="ctaLabel" :helper="helper" :title="title" />

    <TransactionBudgetAlert
      v-if="!isIncome && hasBudgetLimit"
      :mode-label="budgetModeLabel"
      :remaining="budgetSnapshot.remaining"
      :usage="budgetUsage"
    />

    <TransactionFilters
      v-model:category-id="filters.categoryId"
      v-model:date-from="filters.dateFrom"
      v-model:date-to="filters.dateTo"
      :category-options="categoryOptions"
      :is-income="isIncome"
      @apply="applyFilters"
      @reset="resetFilters"
    />

    <p v-if="errorMessage" class="page-error" role="alert">{{ errorMessage }}</p>

    <div class="split-grid">
      <TransactionTable
        :is-income="isIncome"
        :pagination="pagination"
        :total="total"
        :transactions="visibleTransactions"
        @delete="removeTransaction"
        @edit="startEdit"
        @page="changePage"
      />
      <TransactionQuickForm
        :category-options="categoryOptions"
        :cta-label="ctaLabel"
        :editing-transaction="editingTransaction"
        :is-income="isIncome"
        :is-saving="isLoading"
        @cancel="cancelEdit"
        @save="saveTransaction"
      />
    </div>
  </section>
</template>

<style scoped>
.page-stack {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.split-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  align-items: start;
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
  .split-grid {
    grid-template-columns: 1fr;
  }
}
</style>

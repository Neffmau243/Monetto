<script setup lang="ts">
import { shallowRef } from 'vue'
import TransactionBudgetAlert from '../components/transactions/TransactionBudgetAlert.vue'
import TransactionFilters from '../components/transactions/TransactionFilters.vue'
import TransactionFormDialog from '../components/transactions/TransactionFormDialog.vue'
import TransactionHeader from '../components/transactions/TransactionHeader.vue'
import TransactionTable from '../components/transactions/TransactionTable.vue'
import { useTransactionScreen } from '../composables/useTransactionScreen'
import type { Transaction, TransactionFormPayload, TransactionType } from '../types'

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

const isFormDialogOpen = shallowRef(false)

function openCreateDialog() {
  cancelEdit()
  isFormDialogOpen.value = true
}

function openEditDialog(transaction: Transaction) {
  startEdit(transaction)
  isFormDialogOpen.value = true
}

function closeFormDialog() {
  cancelEdit()
  isFormDialogOpen.value = false
}

async function handleSaveTransaction(payload: TransactionFormPayload) {
  const wasSaved = await saveTransaction(payload)

  if (wasSaved) {
    isFormDialogOpen.value = false
  }
}
</script>

<template>
  <section class="page-stack transaction-page" :class="isIncome ? 'income-view' : 'expense-view'">
    <TransactionHeader
      :count="pagination.total"
      :cta-label="ctaLabel"
      :helper="helper"
      :is-income="isIncome"
      :title="title"
      :total="total"
      @create="openCreateDialog"
    />

    <TransactionBudgetAlert
      v-if="!isIncome && hasBudgetLimit"
      :mode-label="budgetModeLabel"
      :remaining="budgetSnapshot.remaining"
      :usage="budgetUsage"
    />

    <div class="transaction-workspace">
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

      <TransactionTable
        :is-income="isIncome"
        :pagination="pagination"
        :total="total"
        :transactions="visibleTransactions"
        @delete="removeTransaction"
        @edit="openEditDialog"
        @page="changePage"
      />
    </div>

    <TransactionFormDialog
      :category-options="categoryOptions"
      :cta-label="ctaLabel"
      :editing-transaction="editingTransaction"
      :is-income="isIncome"
      :is-open="isFormDialogOpen"
      :is-saving="isLoading"
      @close="closeFormDialog"
      @save="handleSaveTransaction"
    />
  </section>
</template>

<style scoped>
.transaction-workspace {
  display: grid;
  min-width: 0;
  gap: 18px;
}

.page-error {
  padding: 12px 14px;
  border: 1px solid rgba(255, 109, 122, 0.28);
  border-radius: var(--radius);
  background: var(--danger-soft);
  color: var(--danger);
  font-weight: 800;
}

</style>

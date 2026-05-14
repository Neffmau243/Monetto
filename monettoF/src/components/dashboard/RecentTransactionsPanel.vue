<script setup lang="ts">
import AppIcon from '../AppIcon.vue'
import type { Transaction } from '../../types'
import { formatDate, formatTransactionAmount } from '../../utils/formatters'

defineProps<{
  transactions: Transaction[]
}>()
</script>

<template>
  <article class="panel panel-wide">
    <div class="panel-heading">
      <div>
        <h3>Últimos movimientos</h3>
        <p>Transacciones ordenadas por fecha.</p>
      </div>
    </div>
    <div v-if="transactions.length === 0" class="empty-state">
      Sin movimientos registrados.
    </div>
    <div v-else class="activity-list">
      <div v-for="transaction in transactions" :key="transaction.id" class="activity-row">
        <div class="activity-icon" :class="transaction.type.toLowerCase()">
          <AppIcon :name="transaction.type === 'INCOME' ? 'south_west' : 'north_east'" :size="20" />
        </div>
        <div>
          <strong>{{ transaction.description }}</strong>
          <span>{{ formatDate(transaction.date) }} · {{ transaction.category }}</span>
        </div>
        <strong :class="transaction.type === 'INCOME' ? 'money-income' : 'money-expense'">
          {{ formatTransactionAmount(transaction.amount, transaction.type) }}
        </strong>
      </div>
    </div>
  </article>
</template>

<style scoped>
.panel-wide {
  grid-column: span 2;
}

.activity-list {
  display: grid;
  gap: 8px;
}

.activity-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px;
  border-bottom: 1px solid rgba(51, 215, 218, 0.14);
  border-radius: var(--radius);
  transition: background 160ms ease;
}

.activity-row:hover {
  background: var(--surface-low);
}

.activity-row:last-child {
  border-bottom: 0;
}

.activity-row > div:nth-child(2) {
  display: grid;
  flex: 1;
  min-width: 0;
}

.activity-row span {
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 700;
}

.activity-row strong:last-child {
  text-align: right;
  white-space: nowrap;
}

.activity-icon {
  display: grid;
  width: 40px;
  height: 40px;
  place-items: center;
  border-radius: var(--radius);
}

.activity-icon.income {
  background: var(--secondary-soft);
  color: var(--secondary);
}

.activity-icon.expense {
  background: var(--danger-soft);
  color: var(--danger);
}

@media (max-width: 560px) {
  .activity-row {
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .activity-row strong:last-child {
    width: 100%;
    text-align: left;
    padding-left: 54px;
  }
}

@media (max-width: 1180px) {
  .panel-wide {
    grid-column: span 2;
  }
}

@media (max-width: 720px) {
  .panel-wide {
    grid-column: auto;
  }
}
</style>

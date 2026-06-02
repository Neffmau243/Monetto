<script setup lang="ts">
import AppIcon from '../AppIcon.vue'
import type { PaginationState, Transaction } from '../../types'
import { formatDate, formatMoney, formatTransactionAmount } from '../../utils/formatters'

defineProps<{
  isIncome: boolean
  pagination: PaginationState
  total: number
  transactions: Transaction[]
}>()

const emit = defineEmits<{
  delete: [transactionId: number]
  edit: [transaction: Transaction]
  page: [page: number]
}>()
</script>

<template>
  <article class="panel table-panel">
    <div class="panel-heading">
      <div>
        <h3>{{ isIncome ? 'Historial de ingresos' : 'Historial de gastos' }}</h3>
        <p>{{ transactions.length }} movimientos visibles en esta pagina.</p>
      </div>
      <div class="table-total">
        <span>Total visible</span>
        <strong :class="isIncome ? 'money-income' : 'money-expense'">
          {{ formatMoney(total) }}
        </strong>
      </div>
    </div>

    <div
      class="table-scroll"
      role="region"
      :aria-label="isIncome ? 'Tabla de ingresos' : 'Tabla de gastos'"
    >
      <table>
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Concepto</th>
            <th>Categoria</th>
            <th class="align-right">Monto</th>
            <th>Estado</th>
            <th class="align-right">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="transactions.length === 0">
            <td colspan="6">
              <div class="empty-state transaction-empty">
                <AppIcon :name="isIncome ? 'savings' : 'receipt_long'" :size="28" />
                <span>Sin movimientos registrados.</span>
              </div>
            </td>
          </tr>
          <tr v-for="transaction in transactions" :key="transaction.id">
            <td>{{ formatDate(transaction.date) }}</td>
            <td class="strong-cell">{{ transaction.description || 'Sin descripcion' }}</td>
            <td>
              <span class="chip" :class="isIncome ? 'income' : 'expense'">
                {{ transaction.category }}
              </span>
            </td>
            <td class="align-right" :class="isIncome ? 'money-income' : 'money-expense'">
              {{ formatTransactionAmount(transaction.amount, transaction.type) }}
            </td>
            <td>
              <span class="status-chip">{{ transaction.status }}</span>
            </td>
            <td class="align-right row-actions-cell">
              <button class="icon-button" type="button" aria-label="Editar movimiento" @click="emit('edit', transaction)">
                <AppIcon name="edit" :size="20" />
              </button>
              <button
                class="icon-button danger"
                type="button"
                aria-label="Eliminar movimiento"
                @click="emit('delete', transaction.id)"
              >
                <AppIcon name="delete" :size="20" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination-row">
      <span>Pagina {{ pagination.page }} de {{ pagination.totalPages }} - {{ pagination.total }} movimientos</span>
      <div>
        <button
          class="secondary-action"
          type="button"
          :disabled="!pagination.hasPrevious"
          @click="emit('page', pagination.page - 1)"
        >
          Anterior
        </button>
        <button
          class="secondary-action"
          type="button"
          :disabled="!pagination.hasNext"
          @click="emit('page', pagination.page + 1)"
        >
          Siguiente
        </button>
      </div>
    </div>
  </article>
</template>

<style scoped>
.table-panel {
  padding: 0;
  overflow: hidden;
}

.table-panel .panel-heading {
  margin: 0;
  padding: 22px 24px;
}

.table-total {
  display: grid;
  justify-items: end;
  gap: 2px;
  text-align: right;
}

.table-total span {
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.table-total strong {
  font-size: 22px;
  line-height: 1.15;
  font-variant-numeric: tabular-nums;
}

.table-scroll {
  overflow-x: auto;
}

.transaction-empty {
  gap: 8px;
  color: var(--text-muted);
}

.transaction-empty .app-icon {
  color: var(--primary-strong);
}

.row-actions-cell {
  white-space: nowrap;
}

.pagination-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 24px 20px;
  border-top: 1px solid rgba(51, 215, 218, 0.14);
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 800;
}

.pagination-row > div {
  display: flex;
  gap: 10px;
}

@media (max-width: 720px) {
  .table-panel .panel-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .table-total {
    justify-items: start;
    text-align: left;
  }

  .pagination-row {
    align-items: stretch;
    flex-direction: column;
  }

  .pagination-row > div,
  .pagination-row button {
    width: 100%;
  }
}
</style>

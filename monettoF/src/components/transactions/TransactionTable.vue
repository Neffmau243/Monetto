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
        <p>{{ transactions.length }} movimientos visibles.</p>
      </div>
      <strong :class="isIncome ? 'money-income' : 'money-expense'">
        {{ formatMoney(total) }}
      </strong>
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
              <div class="empty-state">Sin movimientos registrados.</div>
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

.table-scroll {
  overflow-x: auto;
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

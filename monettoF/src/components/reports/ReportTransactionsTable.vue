<script setup lang="ts">
import type { Transaction } from '../../types'
import { formatDate, formatTransactionAmount } from '../../utils/formatters'

defineProps<{
  transactions: Transaction[]
}>()
</script>

<template>
  <article class="panel table-panel">
    <div class="panel-heading">
      <div>
        <h3>Resumen de transacciones del periodo</h3>
        <p>Movimientos incluidos en el reporte seleccionado.</p>
      </div>
    </div>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Descripción</th>
            <th>Categoría</th>
            <th class="align-right">Monto</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="transactions.length === 0">
            <td colspan="4">
              <div class="empty-state">Sin transacciones para este periodo.</div>
            </td>
          </tr>
          <tr v-for="transaction in transactions" :key="transaction.id">
            <td>{{ formatDate(transaction.date) }}</td>
            <td class="strong-cell">{{ transaction.description }}</td>
            <td>
              <span class="chip" :class="transaction.type === 'INCOME' ? 'income' : 'expense'">
                {{ transaction.category }}
              </span>
            </td>
            <td
              class="align-right"
              :class="transaction.type === 'INCOME' ? 'money-income' : 'money-expense'"
            >
              {{ formatTransactionAmount(transaction.amount, transaction.type) }}
            </td>
          </tr>
        </tbody>
      </table>
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
</style>

<script setup lang="ts">
import AppIcon from '../AppIcon.vue'
import { formatMoney } from '../../utils/formatters'

defineProps<{
  count: number
  ctaLabel: string
  helper: string
  isIncome: boolean
  title: string
  total: number
}>()

const emit = defineEmits<{
  create: []
}>()
</script>

<template>
  <header class="transaction-header" :class="isIncome ? 'income' : 'expense'">
    <div class="transaction-title-block">
      <span class="section-kicker">
        <AppIcon :name="isIncome ? 'trending_up' : 'trending_down'" :size="18" />
        {{ isIncome ? 'Capital entrante' : 'Control de salidas' }}
      </span>
      <h2>{{ title }}</h2>
      <p>{{ helper }}</p>
    </div>

    <div class="transaction-summary-card">
      <span>Total visible</span>
      <strong :class="isIncome ? 'money-income' : 'money-expense'">{{ formatMoney(total) }}</strong>
      <small>{{ count }} movimientos encontrados</small>
      <button class="primary-inline-action" type="button" @click="emit('create')">
        <AppIcon name="add_circle" :size="20" />
        {{ ctaLabel }}
      </button>
    </div>
  </header>
</template>

<style scoped>
.transaction-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, 340px);
  align-items: stretch;
  gap: 24px;
  padding: 24px;
  overflow: hidden;
  border: 1px solid rgba(51, 215, 218, 0.2);
  border-radius: var(--radius);
  background:
    linear-gradient(135deg, rgba(8, 239, 245, 0.1), rgba(7, 28, 32, 0.96) 46%),
    var(--surface);
  box-shadow: var(--shadow-soft);
}

.transaction-header.expense {
  background:
    linear-gradient(135deg, rgba(255, 109, 122, 0.12), rgba(7, 28, 32, 0.96) 46%),
    var(--surface);
}

.transaction-title-block {
  display: grid;
  align-content: center;
  min-width: 0;
  gap: 10px;
}

.section-kicker {
  display: inline-flex;
  width: fit-content;
  min-height: 32px;
  align-items: center;
  gap: 8px;
  padding: 0 10px;
  border: 1px solid rgba(51, 215, 218, 0.2);
  border-radius: 999px;
  background: var(--primary-soft);
  color: var(--primary-strong);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.transaction-header.expense .section-kicker {
  border-color: rgba(255, 109, 122, 0.24);
  background: var(--danger-soft);
  color: var(--danger);
}

.transaction-header h2 {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.25;
}

.transaction-header p {
  max-width: 620px;
  color: var(--text-muted);
}

.transaction-summary-card {
  display: grid;
  gap: 8px;
  padding: 18px;
  border: 1px solid rgba(51, 215, 218, 0.18);
  border-radius: var(--radius);
  background: rgba(3, 17, 20, 0.58);
}

.transaction-summary-card span,
.transaction-summary-card small {
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 800;
}

.transaction-summary-card strong {
  font-size: 30px;
  line-height: 1.12;
  font-variant-numeric: tabular-nums;
  word-break: break-word;
}

.transaction-summary-card .primary-inline-action {
  margin-top: 8px;
}

@media (max-width: 900px) {
  .transaction-header {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .transaction-header {
    padding: 20px;
  }

  .transaction-header h2 {
    font-size: 28px;
  }
}
</style>

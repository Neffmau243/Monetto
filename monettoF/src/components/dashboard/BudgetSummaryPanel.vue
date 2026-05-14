<script setup lang="ts">
import { formatMoney, percent } from '../../utils/formatters'

defineProps<{
  limit: string
  modeDetail: string
  modeLabel: string
  remaining: string
  spent: string
  usage: number
}>()
</script>

<template>
  <article class="panel">
    <div class="panel-heading">
      <div>
        <h3>Presupuesto mensual</h3>
        <p>{{ modeLabel }}</p>
      </div>
      <strong class="metric">{{ percent(usage) }}</strong>
    </div>
    <div class="meter budget">
      <span :style="{ width: `${usage}%` }"></span>
    </div>
    <div class="budget-line">
      <span>Gastado {{ formatMoney(spent) }}</span>
      <span>Limite {{ formatMoney(limit) }}</span>
    </div>
    <p class="budget-detail">{{ modeDetail }} Disponible: {{ formatMoney(remaining) }}.</p>
  </article>
</template>

<style scoped>
.budget-line {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 12px;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 700;
}

.budget-detail {
  margin-top: 10px;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 700;
}
</style>

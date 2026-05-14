<script setup lang="ts">
import { computed } from 'vue'
import { formatMoney, percent } from '../../utils/formatters'

const props = defineProps<{
  budgetModeLabel: string
  budgetRemaining: string
  budgetUsage: number
  netResult: number
  savingRate: number
}>()

const isDeficit = computed(() => props.netResult < 0)
const visualRate = computed(() => Math.max(0, Math.min(100, props.savingRate)))
const title = computed(() => (isDeficit.value ? 'Deficit del periodo' : 'Tasa de ahorro'))
const helper = computed(() =>
  isDeficit.value
    ? `Los gastos superan ingresos por ${formatMoney(Math.abs(props.netResult))}.`
    : `Ahorraste ${formatMoney(props.netResult)} este mes.`,
)
</script>

<template>
  <article class="panel saving-panel" :class="{ deficit: isDeficit }">
    <div class="panel-heading">
      <div>
        <h3>{{ title }}</h3>
        <p>{{ helper }}</p>
      </div>
      <strong class="metric">{{ savingRate }}%</strong>
    </div>
    <div class="meter">
      <span :style="{ width: `${visualRate}%` }"></span>
    </div>
    <p class="budget-note">
      {{ budgetModeLabel }}: {{ percent(budgetUsage) }} usado, {{ formatMoney(budgetRemaining) }}
      disponible.
    </p>
  </article>
</template>

<style scoped>
.budget-note {
  margin-top: 12px;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 700;
}

.saving-panel.deficit .metric,
.saving-panel.deficit h3 {
  color: var(--danger);
}

.saving-panel.deficit .meter span {
  background: var(--danger);
}
</style>

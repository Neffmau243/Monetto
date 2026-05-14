<script setup lang="ts">
import { computed } from 'vue'
import { formatMoney } from '../../utils/formatters'

const props = defineProps<{
  expenseTotal: number
  incomeTotal: number
  netResult: number
}>()

const resultTone = computed(() => (props.netResult < 0 ? 'negative' : 'positive'))
</script>

<template>
  <article class="report-hero" :class="resultTone">
    <span>Resultado neto del periodo</span>
    <strong>{{ formatMoney(netResult, 'auto') }}</strong>
    <p>{{ formatMoney(incomeTotal) }} en ingresos · {{ formatMoney(expenseTotal) }} en gastos</p>
    <svg viewBox="0 0 600 150" role="img" aria-label="Curva de resultado mensual">
      <path
        d="M0 118 C95 72 146 92 218 66 C300 36 354 78 429 42 C496 12 548 28 600 20"
        fill="none"
        stroke="currentColor"
        stroke-linecap="round"
        stroke-width="5"
      />
      <path
        d="M0 118 C95 72 146 92 218 66 C300 36 354 78 429 42 C496 12 548 28 600 20 L600 150 L0 150 Z"
        fill="currentColor"
        opacity=".1"
      />
    </svg>
  </article>
</template>

<style scoped>
.report-hero {
  display: flex;
  min-height: 304px;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  padding: 30px;
  border: 1px solid rgba(8, 239, 245, 0.28);
  border-radius: var(--radius);
  background:
    radial-gradient(circle at 20% 14%, rgba(8, 239, 245, 0.24), transparent 34%),
    linear-gradient(160deg, #092328 0%, #071c20 50%, #041317 100%);
  color: var(--text);
  box-shadow: var(--shadow);
}

.report-hero span {
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
}

.report-hero strong {
  display: block;
  margin-top: 10px;
  color: var(--text);
  font-size: 44px;
  line-height: 1.12;
}

.report-hero p {
  margin-top: 12px;
  color: var(--text-muted);
}

.report-hero svg {
  width: 100%;
  color: rgba(8, 239, 245, 0.58);
}

.report-hero.positive strong {
  color: var(--secondary);
}

.report-hero.negative {
  border-color: rgba(255, 109, 122, 0.36);
}

.report-hero.negative strong,
.report-hero.negative svg {
  color: var(--danger);
}

@media (max-width: 1180px) {
  .report-hero {
    grid-column: span 2;
  }
}

@media (max-width: 720px) {
  .report-hero {
    grid-column: auto;
  }

  .report-hero strong {
    font-size: 32px;
  }
}
</style>

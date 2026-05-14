<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import AppIcon from '../AppIcon.vue'
import { clampPercent, formatMoney, percent } from '../../utils/formatters'

const props = defineProps<{
  balance: number
  budgetRemaining: string
  budgetUsage: number
  expenseTotal: number
  incomeTotal: number
}>()

const hasFinancialData = computed(
  () => props.incomeTotal > 0 || props.expenseTotal > 0 || props.balance !== 0 || props.budgetUsage > 0,
)
const normalizedBudgetUsage = computed(() => clampPercent(props.budgetUsage))
const healthScore = computed(() => {
  if (!hasFinancialData.value) {
    return 0
  }

  const deficitPenalty = props.balance < 0 ? 34 : 0

  return Math.max(0, Math.min(100, Math.round(100 - normalizedBudgetUsage.value * 0.34 - deficitPenalty)))
})

const netFlow = computed(() => props.incomeTotal - props.expenseTotal)
const healthTone = computed(() => {
  if (props.balance < 0 || normalizedBudgetUsage.value >= 100) {
    return 'critical'
  }

  if (normalizedBudgetUsage.value >= 85 || healthScore.value < 70) {
    return 'warning'
  }

  return 'success'
})
const budgetMood = computed(() => {
  if (!hasFinancialData.value) {
    return 'Sin datos registrados'
  }

  if (props.balance < 0) {
    return 'Deficit critico'
  }

  if (normalizedBudgetUsage.value >= 100) {
    return 'Presupuesto agotado'
  }

  return normalizedBudgetUsage.value >= 85 ? 'Atencion requerida' : 'Ritmo saludable'
})
const scoreRingOffset = computed(() => 100 - healthScore.value)
</script>

<template>
  <article class="dashboard-hero">
    <div class="hero-copy">
      <span class="hero-eyebrow">
        <AppIcon name="verified" :size="18" />
        Resumen disponible
      </span>
      <h2>Tu panorama financiero está listo para decidir mejor.</h2>
      <p>
        Balance, presupuesto y movimientos viven en una sola vista para que detectes fugas,
        protejas tu margen y cierres el mes con intención.
      </p>
      <div class="hero-actions">
        <RouterLink class="primary-inline-action" to="/expenses">
          <AppIcon name="add" :size="20" />
          Registrar gasto
        </RouterLink>
        <RouterLink class="secondary-action" to="/reports">
          <AppIcon name="monitoring" :size="20" />
          Ver reporte
        </RouterLink>
      </div>
    </div>

    <div class="hero-summary" aria-label="Resumen de salud financiera">
      <div class="score-block">
        <div class="score-ring" :class="healthTone" aria-hidden="true">
          <svg class="score-ring-svg" viewBox="0 0 100 100" focusable="false">
            <circle class="score-ring-track" cx="50" cy="50" r="42" pathLength="100" />
            <circle
              class="score-ring-progress"
              cx="50"
              cy="50"
              r="42"
              pathLength="100"
              :stroke-dashoffset="scoreRingOffset"
            />
          </svg>
          <span class="score-value">{{ healthScore }}</span>
        </div>
        <div class="score-copy">
          <strong>{{ budgetMood }}</strong>
          <span>{{ percent(normalizedBudgetUsage) }} del presupuesto usado</span>
        </div>
      </div>

      <dl class="summary-list">
        <div>
          <dt>Balance actual</dt>
          <dd :class="healthTone === 'critical' ? 'money-expense' : healthTone === 'warning' ? 'money-warning' : 'money-income'">
            {{ formatMoney(balance, 'auto') }}
          </dd>
        </div>
        <div>
          <dt>Flujo neto</dt>
          <dd :class="netFlow >= 0 ? 'money-income' : 'money-expense'">
            {{ formatMoney(netFlow, 'auto') }}
          </dd>
        </div>
        <div>
          <dt>Disponible</dt>
          <dd>{{ formatMoney(budgetRemaining) }}</dd>
        </div>
      </dl>
    </div>
  </article>
</template>

<style scoped>
.dashboard-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(360px, 0.92fr);
  gap: 24px;
  padding: 24px;
  overflow: hidden;
  border: 1px solid rgba(8, 239, 245, 0.28);
  border-radius: var(--radius);
  background:
    radial-gradient(circle at 16% 14%, rgba(8, 239, 245, 0.24), transparent 34%),
    linear-gradient(145deg, rgba(9, 37, 42, 0.98), rgba(5, 20, 24, 0.98));
  box-shadow: var(--shadow);
}

.hero-copy {
  display: flex;
  min-width: 0;
  flex-direction: column;
  justify-content: center;
}

.hero-eyebrow,
.hero-actions,
.score-block {
  display: flex;
  align-items: center;
}

.hero-eyebrow {
  width: fit-content;
  gap: 8px;
  padding: 7px 10px;
  border: 1px solid rgba(8, 239, 245, 0.28);
  border-radius: 999px;
  background: var(--primary-soft);
  color: var(--primary-strong);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.hero-copy h2 {
  max-width: 620px;
  margin-top: 18px;
  font-size: clamp(28px, 3vw, 40px);
  line-height: 1.1;
}

.hero-copy p {
  max-width: 620px;
  margin-top: 16px;
  color: var(--text-muted);
  font-size: 16px;
}

.hero-actions {
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
}

.hero-summary {
  display: grid;
  align-content: center;
  gap: 22px;
  min-width: 0;
  padding: 18px 0 18px 24px;
  border-left: 1px solid rgba(8, 239, 245, 0.24);
}

.score-block {
  gap: 16px;
}

.score-ring {
  position: relative;
  display: grid;
  width: 92px;
  aspect-ratio: 1;
  flex: 0 0 auto;
  place-items: center;
}

.score-ring-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
  transform: rotate(-90deg);
}

.score-ring-track,
.score-ring-progress {
  fill: none;
  stroke-width: 18;
}

.score-ring-track {
  stroke: var(--surface-mid);
}

.score-ring-progress {
  stroke: var(--primary);
  stroke-dasharray: 100;
  stroke-linecap: round;
  transition: stroke-dashoffset 220ms ease;
}

.score-ring.success .score-ring-progress {
  stroke: var(--secondary);
}

.score-ring.warning .score-ring-progress {
  stroke: var(--warning);
}

.score-ring.critical .score-ring-progress {
  stroke: var(--danger);
}

.score-ring.warning .score-value {
  color: var(--warning);
}

.score-ring.critical .score-value {
  color: var(--danger);
}

.score-ring .score-value {
  position: relative;
  z-index: 1;
  display: grid;
  width: 64px;
  aspect-ratio: 1;
  place-items: center;
  border-radius: 50%;
  background: var(--surface);
  color: var(--primary-strong);
  font-size: 25px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  box-shadow: inset 0 0 0 1px var(--outline);
}

.score-copy strong,
.score-copy span {
  display: block;
}

.score-copy strong {
  font-size: 20px;
  line-height: 1.2;
}

.score-copy span {
  margin-top: 4px;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 700;
}

.summary-list {
  display: grid;
  gap: 0;
  margin: 0;
  border-top: 1px solid var(--outline);
}

.summary-list div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0;
  border-bottom: 1px solid var(--outline);
}

.summary-list dt {
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 800;
}

.summary-list dd {
  margin: 0;
  color: var(--text);
  font-size: 18px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  text-align: right;
}

.money-warning {
  color: var(--warning);
}

@media (max-width: 1180px) {
  .dashboard-hero {
    grid-template-columns: 1fr;
  }

  .hero-summary {
    padding: 22px 0 0;
    border-top: 1px solid rgba(8, 239, 245, 0.24);
    border-left: 0;
  }
}

@media (max-width: 720px) {
  .dashboard-hero {
    padding: 22px;
  }

  .score-block {
    align-items: flex-start;
  }

  .score-ring {
    width: 88px;
  }

  .score-ring .score-value {
    width: 62px;
    font-size: 24px;
  }

  .summary-list div {
    align-items: flex-start;
    flex-direction: column;
    gap: 4px;
  }

  .summary-list dd {
    text-align: left;
  }
}
</style>

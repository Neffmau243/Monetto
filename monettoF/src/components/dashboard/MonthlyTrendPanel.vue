<script setup lang="ts">
import AppIcon from '../AppIcon.vue'
import type { DashboardTrendPoint } from '../../composables/useDashboardSummary'

defineProps<{
  points: DashboardTrendPoint[]
}>()
</script>

<template>
  <article class="panel panel-wide">
    <div class="panel-heading">
      <div>
        <h3>Tendencia mensual</h3>
        <p>Mes actual y periodos donde ya existe flujo registrado.</p>
      </div>
      <AppIcon name="stacked_line_chart" :size="24" />
    </div>
    <div v-if="points.length === 0" class="empty-state">
      Sin tendencia mensual registrada.
    </div>
    <div v-else class="chart-legend" aria-hidden="true">
      <span><i class="income"></i>Ingresos</span>
      <span><i class="expense"></i>Gastos</span>
    </div>
    <div v-if="points.length > 0" class="trend-chart" role="img" aria-label="Tendencia mensual de ingresos y gastos">
      <div v-for="point in points" :key="point.month" class="trend-column" :class="{ current: point.isCurrent }">
        <div class="trend-bars">
          <span class="bar income" :style="{ height: `${point.incomeHeight}px` }"></span>
          <span class="bar expense" :style="{ height: `${point.expenseHeight}px` }"></span>
        </div>
        <span>{{ point.monthLabel }}</span>
      </div>
    </div>
  </article>
</template>

<style scoped>
.panel-wide {
  grid-column: span 2;
}

.trend-chart {
  display: grid;
  min-height: 240px;
  grid-template-columns: repeat(auto-fit, minmax(72px, 1fr));
  align-items: end;
  gap: 18px;
  padding-top: 20px;
  background:
    linear-gradient(to top, rgba(51, 215, 218, 0.12) 1px, transparent 1px) 0 20px / 100% 48px;
}

.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 800;
}

.chart-legend span {
  display: inline-flex;
  align-items: center;
  gap: 7px;
}

.chart-legend i {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.chart-legend i.income {
  background: var(--secondary);
}

.chart-legend i.expense {
  background: var(--danger);
}

.trend-column {
  display: grid;
  gap: 10px;
  justify-items: center;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 800;
}

.trend-column.current > span {
  color: var(--primary-strong);
}

.trend-bars {
  display: flex;
  height: 190px;
  align-items: end;
  gap: 8px;
}

.bar {
  display: block;
  width: 20px;
  min-height: 20px;
  border-radius: 6px 6px 2px 2px;
  box-shadow: inset 0 -10px 16px rgba(255, 255, 255, 0.16);
}

.bar.income {
  background: linear-gradient(180deg, #31b77e, var(--secondary));
}

.bar.expense {
  background: linear-gradient(180deg, #de6670, var(--danger));
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

  .trend-chart {
    gap: 8px;
    overflow-x: auto;
  }
}
</style>

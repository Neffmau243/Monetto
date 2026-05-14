<script setup lang="ts">
import AppIcon from '../AppIcon.vue'
import { formatMoney, percent } from '../../utils/formatters'

defineProps<{
  modeLabel: string
  remaining: string
  usage: number
}>()
</script>

<template>
  <section class="alert-panel" role="status" aria-live="polite">
    <div class="alert-icon">
      <AppIcon name="warning" :size="24" />
    </div>
    <div>
      <h3>Alerta de presupuesto mensual</h3>
      <p>
        Has alcanzado el {{ percent(usage) }} de tu {{ modeLabel }}. Quedan
        {{ formatMoney(remaining) }} disponibles.
      </p>
      <div class="meter danger">
        <span :style="{ width: `${usage}%` }"></span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.alert-panel {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 16px;
  padding: 18px;
  border: 1px solid rgba(194, 65, 75, 0.24);
  border-radius: var(--radius);
  background: var(--danger-soft);
  box-shadow: var(--shadow-soft);
}

.alert-panel h3 {
  margin-bottom: 4px;
  font-size: 16px;
}

.alert-panel p {
  margin-bottom: 12px;
  color: var(--text-muted);
}

.alert-icon {
  display: grid;
  width: 44px;
  height: 44px;
  place-items: center;
  border-radius: var(--radius);
  background: var(--danger-soft);
  color: var(--danger);
}
</style>

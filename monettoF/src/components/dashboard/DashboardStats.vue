<script setup lang="ts">
import StatCard from '../ui/StatCard.vue'
import type { DashboardStat } from '../../composables/useDashboardSummary'

defineProps<{
  stats: DashboardStat[]
}>()
</script>

<template>
  <div class="stats-grid">
    <StatCard
      v-for="stat in stats"
      :key="stat.label"
      :label="stat.label"
      :value="stat.value"
      :icon="stat.icon"
      :tone="stat.tone"
      :detail="stat.detail"
    />
  </div>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

@media (max-width: 1180px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>

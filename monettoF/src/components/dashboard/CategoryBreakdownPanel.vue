<script setup lang="ts">
import { percent } from '../../utils/formatters'

interface CategoryBreakdownItem {
  label: string
  percent: number
  color: string
}

defineProps<{
  categories: CategoryBreakdownItem[]
}>()
</script>

<template>
  <article class="panel">
    <div class="panel-heading">
      <div>
        <h3>Gastos por categoría</h3>
        <p>Distribución del mes actual.</p>
      </div>
    </div>
    <div v-if="categories.length === 0" class="empty-state">
      Sin gastos por categoria.
    </div>
    <div v-else class="category-list" role="list">
      <div v-for="category in categories" :key="category.label" class="category-row" role="listitem">
        <div>
          <span class="color-dot" :style="{ background: category.color }"></span>
          <strong>{{ category.label }}</strong>
        </div>
        <span>{{ percent(category.percent) }}</span>
        <div class="meter small" role="img" :aria-label="`${category.label}: ${percent(category.percent)}`">
          <span :style="{ width: `${category.percent}%`, background: category.color }"></span>
        </div>
      </div>
    </div>
  </article>
</template>

<style scoped>
.category-list {
  display: grid;
  gap: 14px;
}

.category-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px 12px;
  padding: 2px 0;
}

.category-row > div {
  display: flex;
  align-items: center;
  gap: 8px;
}

.category-row span {
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 700;
}

.category-row strong {
  font-size: 14px;
}

.color-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(20, 33, 30, 0.05);
}
</style>

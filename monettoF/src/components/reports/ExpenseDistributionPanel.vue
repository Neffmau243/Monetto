<script setup lang="ts">
import { formatMoney } from '../../utils/formatters'

interface ExpenseCategory {
  label: string
  value: number
  color: string
}

defineProps<{
  categories: ExpenseCategory[]
}>()
</script>

<template>
  <article class="panel">
    <div class="panel-heading">
      <div>
        <h3>Distribución de gastos</h3>
        <p>Categorías principales del periodo.</p>
      </div>
    </div>
    <div v-if="categories.length === 0" class="empty-state">
      Sin categorias de gasto registradas.
    </div>
    <div v-else class="donut-summary">
      <div class="donut" role="img" aria-label="Distribución visual de gastos">
        <span>Top</span>
      </div>
      <div class="category-list compact">
        <div v-for="category in categories" :key="category.label" class="category-row">
          <div>
            <span class="color-dot" :style="{ background: category.color }"></span>
            <strong>{{ category.label }}</strong>
          </div>
          <span>{{ formatMoney(category.value) }}</span>
        </div>
      </div>
    </div>
  </article>
</template>

<style scoped>
.donut-summary {
  display: grid;
  grid-template-columns: 150px minmax(0, 1fr);
  gap: 20px;
  align-items: center;
}

.donut {
  display: grid;
  width: 150px;
  aspect-ratio: 1;
  place-items: center;
  border-radius: 50%;
  background: conic-gradient(
    var(--primary) 0 72%,
    var(--danger) 72% 93%,
    var(--secondary) 93% 97%,
    var(--tertiary) 97% 100%
  );
  box-shadow: inset 0 0 0 34px var(--surface);
}

.donut span {
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.category-list {
  display: grid;
  gap: 10px;
}

.category-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px 12px;
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

.color-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

@media (max-width: 720px) {
  .donut-summary {
    grid-template-columns: 1fr;
  }

  .donut {
    justify-self: center;
  }
}
</style>

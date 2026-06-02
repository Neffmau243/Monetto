<script setup lang="ts">
import AppIcon from '../AppIcon.vue'
import type { Category } from '../../types'

defineProps<{
  categoryOptions: Category[]
  isIncome: boolean
}>()

const categoryId = defineModel<string>('categoryId', { required: true })
const dateFrom = defineModel<string>('dateFrom', { required: true })
const dateTo = defineModel<string>('dateTo', { required: true })

const emit = defineEmits<{
  apply: []
  reset: []
}>()
</script>

<template>
  <section class="filters-panel" aria-label="Filtros de transacciones">
    <div class="filters-title">
      <AppIcon name="tune" :size="20" />
      <div>
        <strong>Filtros</strong>
        <span>{{ isIncome ? 'Afina ingresos por fecha o categoria' : 'Afina gastos por fecha o categoria' }}</span>
      </div>
    </div>
    <label>
      <span>Rango de fechas</span>
      <div class="date-row">
        <input v-model="dateFrom" type="date" />
        <input v-model="dateTo" type="date" />
      </div>
    </label>
    <label>
      <span>{{ isIncome ? 'Categoria de ingreso' : 'Categoria de gasto' }}</span>
      <select v-model="categoryId">
        <option value="">Todas las categorias</option>
        <option v-for="category in categoryOptions" :key="category.id" :value="String(category.id)">
          {{ category.name }}
        </option>
      </select>
    </label>
    <div class="filter-actions">
      <button class="secondary-action" type="button" @click="emit('apply')">
        <AppIcon name="filter_list" :size="20" />
        Aplicar
      </button>
      <button class="icon-button boxed" type="button" aria-label="Restablecer filtros" @click="emit('reset')">
        <AppIcon name="refresh" :size="20" />
      </button>
    </div>
  </section>
</template>

<style scoped>
.filters-panel {
  display: grid;
  grid-template-columns: minmax(180px, 0.8fr) minmax(280px, 1.2fr) minmax(220px, 1fr) auto;
  align-items: end;
  gap: 16px;
  padding: 18px;
  border: 1px solid rgba(51, 215, 218, 0.16);
  border-radius: var(--radius);
  background:
    linear-gradient(180deg, rgba(9, 31, 35, 0.98), rgba(7, 28, 32, 0.98)),
    var(--surface);
  box-shadow: var(--shadow-soft);
}

.filters-title {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 46px;
  color: var(--primary-strong);
}

.filters-title > .app-icon {
  padding: 10px;
  border-radius: var(--radius);
  background: var(--primary-soft);
}

.filters-title strong,
.filters-title span {
  display: block;
}

.filters-title strong {
  color: var(--text);
  font-size: 14px;
  line-height: 1.2;
}

.filters-title span {
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
}

.date-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.filter-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

@media (max-width: 1180px) {
  .filters-panel {
    grid-template-columns: 1fr 1fr;
  }

  .filters-title,
  .filter-actions {
    justify-content: flex-start;
  }
}

@media (max-width: 720px) {
  .filters-panel,
  .date-row {
    grid-template-columns: 1fr;
  }

  .filters-panel {
    align-items: stretch;
  }

  .filter-actions,
  .filter-actions .secondary-action {
    width: 100%;
  }
}
</style>

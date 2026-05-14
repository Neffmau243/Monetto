<script setup lang="ts">
import { computed, onMounted, reactive, shallowRef } from 'vue'
import AppIcon from '../components/AppIcon.vue'
import { useAuthSession } from '../composables/useAuthSession'
import {
  createBudget,
  deleteBudget,
  getBudgets,
  getDashboardSummary,
  updateBudget,
} from '../services/monettoApi'
import { currentBudgetSnapshot, mapBudgetRecord } from '../services/monettoMappers'
import type { BudgetRecord, BudgetSource } from '../types'
import { budgetMonthDate, currentMonth, formatMoney, moneyString, percent, toNumber } from '../utils/formatters'

const { requireToken } = useAuthSession()
const budgetHistory = shallowRef<BudgetRecord[]>([])
const budgetSnapshot = shallowRef(currentBudgetSnapshot())
const budgetSource = shallowRef<BudgetSource | null>(null)
const isLoading = shallowRef(false)
const errorMessage = shallowRef('')
const form = reactive({
  amount: '',
  editingId: null as number | null,
  month: currentMonth(),
})

const hasBudget = computed(() => toNumber(budgetSnapshot.value.limit) > 0)
const budgetUsage = computed(() => {
  const limit = toNumber(budgetSnapshot.value.limit)

  return limit > 0 ? (toNumber(budgetSnapshot.value.spent) / limit) * 100 : 0
})
const budgetState = computed(() => {
  if (!hasBudget.value) {
    return 'Sin presupuesto'
  }

  if (budgetUsage.value >= 100) {
    return 'Excedido'
  }

  return budgetUsage.value > 85 ? 'En riesgo' : 'Saludable'
})
const budgetTone = computed(() => {
  if (!hasBudget.value) {
    return 'empty'
  }

  if (budgetUsage.value >= 100) {
    return 'critical'
  }

  return budgetUsage.value > 85 ? 'warning' : 'success'
})
const budgetModeLabel = computed(() => {
  if (!hasBudget.value) {
    return 'Sin limite activo'
  }

  return budgetSource.value === 'DYNAMIC_INCOME'
    ? 'Capacidad dinamica'
    : 'Presupuesto fijo'
})
const budgetModeHelp = computed(() => {
  if (!hasBudget.value) {
    return 'Registra ingresos o guarda un limite fijo para activar seguimiento.'
  }

  return budgetSource.value === 'DYNAMIC_INCOME'
    ? 'Tus ingresos del mes funcionan como limite mientras no guardes un presupuesto fijo.'
    : 'Este limite fijo se compara contra tus gastos reales del mes.'
})
const canUseDynamicLimit = computed(
  () => budgetSource.value === 'DYNAMIC_INCOME' && !form.editingId && hasBudget.value,
)

async function loadBudgets() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const token = requireToken()
    const [budgets, summary] = await Promise.all([
      getBudgets(token),
      getDashboardSummary(token, currentMonth()),
    ])
    const budgetSummaries = await Promise.all(
      budgets.map((budget) => getDashboardSummary(token, budget.month.slice(0, 7))),
    )

    budgetSource.value = summary.budget_info?.source ?? null
    budgetSnapshot.value = currentBudgetSnapshot(
      summary.budget_info?.amount,
      summary.budget_info?.spent,
      summary.budget_info?.remaining,
    )
    budgetHistory.value = budgets.map((budget, index) =>
      mapBudgetRecord(budget, budgetSummaries[index]?.total_expenses ?? '0.00'),
    )
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudieron cargar presupuestos'
  } finally {
    isLoading.value = false
  }
}

function startEdit(record: BudgetRecord) {
  form.editingId = record.id
  form.month = record.period
  form.amount = record.limit
}

function resetForm() {
  form.editingId = null
  form.month = currentMonth()
  form.amount = ''
}

function useDynamicLimit() {
  form.editingId = null
  form.month = currentMonth()
  form.amount = budgetSnapshot.value.limit
}

async function submitBudget() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const token = requireToken()
    const payload = {
      amount: moneyString(form.amount),
      month: budgetMonthDate(form.month),
    }

    if (form.editingId) {
      await updateBudget(token, form.editingId, payload)
    } else {
      await createBudget(token, payload)
    }

    resetForm()
    await loadBudgets()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo guardar presupuesto'
  } finally {
    isLoading.value = false
  }
}

async function removeBudget(record: BudgetRecord) {
  isLoading.value = true
  errorMessage.value = ''

  try {
    await deleteBudget(requireToken(), record.id)
    await loadBudgets()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo eliminar presupuesto'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  void loadBudgets()
})
</script>

<template>
  <section class="page-stack">
    <header class="page-header">
      <div>
        <h2>Presupuesto mensual</h2>
        <p>Configura y monitorea tus limites para mantener tu salud financiera.</p>
      </div>
      <button class="secondary-action" type="button" :disabled="isLoading" @click="loadBudgets">
        <AppIcon name="refresh" :size="20" />
        Actualizar
      </button>
    </header>

    <p v-if="errorMessage" class="page-error" role="alert">{{ errorMessage }}</p>

    <div class="budget-grid">
      <article class="budget-hero" :class="budgetTone">
        <span>{{ budgetModeLabel }}</span>
        <strong>{{ budgetState }}</strong>
        <p>{{ formatMoney(budgetSnapshot.spent) }} usados de {{ formatMoney(budgetSnapshot.limit) }}</p>
        <p class="budget-mode-help">{{ budgetModeHelp }}</p>
        <div class="meter budget-hero-meter">
          <span :style="{ width: `${Math.min(budgetUsage, 100)}%` }"></span>
        </div>
        <div class="budget-hero-footer">
          <span>{{ percent(budgetUsage) }} ejecutado</span>
          <span>{{ formatMoney(budgetSnapshot.remaining) }} disponibles</span>
        </div>
      </article>

      <article class="panel">
        <div class="panel-heading">
          <div>
            <h3>{{ form.editingId ? 'Editar presupuesto' : 'Configurar presupuesto' }}</h3>
            <p>Guarda un limite fijo si quieres controlar el mes aunque tus ingresos cambien.</p>
          </div>
        </div>
        <form class="compact-form" @submit.prevent="submitBudget">
          <label>
            <span>Mes del presupuesto</span>
            <input v-model="form.month" type="month" required />
          </label>
          <label>
            <span>Limite mensual total</span>
            <input v-model="form.amount" type="number" min="0.01" step="0.01" placeholder="0.00" required />
          </label>
          <button class="submit-button compact" type="submit" :disabled="isLoading">
            {{ form.editingId ? 'Guardar cambios' : 'Guardar presupuesto' }}
          </button>
          <button
            v-if="canUseDynamicLimit"
            class="secondary-action compact-secondary"
            type="button"
            @click="useDynamicLimit"
          >
            Usar ingresos del mes como limite
          </button>
          <button v-if="form.editingId" class="secondary-action compact-secondary" type="button" @click="resetForm">
            Cancelar edicion
          </button>
        </form>
      </article>
    </div>

    <article class="panel table-panel">
      <div class="panel-heading">
        <div>
          <h3>Historico de presupuestos</h3>
          <p>Presupuestos ordenados por mes desde Monetto API.</p>
        </div>
      </div>
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Periodo</th>
              <th>Limite establecido</th>
              <th>Gasto real</th>
              <th>Diferencia</th>
              <th>Estado</th>
              <th class="align-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="budgetHistory.length === 0">
              <td colspan="6">
                <div class="empty-state">Sin presupuestos registrados.</div>
              </td>
            </tr>
            <tr v-for="record in budgetHistory" :key="record.id">
              <td class="strong-cell">{{ record.period }}</td>
              <td>{{ formatMoney(record.limit) }}</td>
              <td>{{ formatMoney(record.spent) }}</td>
              <td :class="toNumber(record.difference) >= 0 ? 'money-income' : 'money-expense'">
                {{ formatMoney(record.difference, 'auto') }}
              </td>
              <td>
                <span class="status-chip" :class="record.status.toLowerCase().replace(' ', '-')">
                  {{ record.status }}
                </span>
              </td>
              <td class="align-right">
                <button class="icon-button" type="button" aria-label="Editar presupuesto" @click="startEdit(record)">
                  <AppIcon name="edit" :size="20" />
                </button>
                <button
                  class="icon-button danger"
                  type="button"
                  aria-label="Eliminar presupuesto"
                  @click="removeBudget(record)"
                >
                  <AppIcon name="delete" :size="20" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>
  </section>
</template>

<style scoped>
.compact-secondary {
  width: 100%;
}

.page-error {
  padding: 12px 14px;
  border: 1px solid rgba(255, 109, 122, 0.28);
  border-radius: var(--radius);
  background: var(--danger-soft);
  color: var(--danger);
  font-weight: 800;
}

.budget-mode-help {
  margin-top: 4px;
  color: var(--text-muted);
  font-size: 13px;
}

.budget-hero.success {
  border-color: rgba(82, 231, 168, 0.34);
}

.budget-hero.success .budget-hero-meter span {
  background: var(--secondary);
}

.budget-hero.warning {
  border-color: rgba(255, 209, 102, 0.38);
}

.budget-hero.warning strong,
.budget-hero.warning .budget-hero-footer span:first-child {
  color: var(--warning);
}

.budget-hero.warning .budget-hero-meter span {
  background: var(--warning);
}

.budget-hero.critical {
  border-color: rgba(255, 109, 122, 0.38);
}

.budget-hero.critical strong,
.budget-hero.critical .budget-hero-footer span:first-child {
  color: var(--danger);
}

.budget-hero.critical .budget-hero-meter span {
  background: var(--danger);
}
</style>

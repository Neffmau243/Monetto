<script setup lang="ts">
import { computed, reactive, watch } from 'vue'
import AppIcon from '../AppIcon.vue'
import type { Category, Transaction, TransactionFormPayload } from '../../types'
import { currentDate, moneyString } from '../../utils/formatters'

const props = defineProps<{
  categoryOptions: Category[]
  ctaLabel: string
  editingTransaction: Transaction | null
  isIncome: boolean
  isSaving: boolean
}>()

const emit = defineEmits<{
  cancel: []
  save: [payload: TransactionFormPayload]
}>()

const form = reactive({
  amount: '',
  categoryId: '',
  date: currentDate(),
  description: '',
})

const formTitle = computed(() => {
  if (props.editingTransaction) {
    return props.isIncome ? 'Editar ingreso' : 'Editar gasto'
  }

  return props.isIncome ? 'Nuevo ingreso' : 'Nuevo gasto rapido'
})

const helperText = computed(() =>
  props.isIncome ? 'Registra capital entrante.' : 'Registra una salida reciente.',
)

watch(
  () => props.editingTransaction,
  (transaction) => {
    form.amount = transaction?.amount ?? ''
    form.categoryId = transaction ? String(transaction.categoryId) : ''
    form.date = transaction?.date ?? currentDate()
    form.description = transaction?.description ?? ''
  },
  { immediate: true },
)

function resetForm() {
  form.amount = ''
  form.categoryId = ''
  form.date = currentDate()
  form.description = ''
}

function submitForm() {
  emit('save', {
    amount: moneyString(form.amount),
    category_id: Number(form.categoryId),
    date: form.date,
    description: form.description.trim() || null,
    type: props.isIncome ? 'INCOME' : 'EXPENSE',
  })

  if (!props.editingTransaction) {
    resetForm()
  }
}
</script>

<template>
  <aside class="panel quick-form-panel" :class="isIncome ? 'income' : 'expense'">
    <div class="quick-form-heading">
      <span class="form-icon" aria-hidden="true">
        <AppIcon :name="isIncome ? 'add_card' : 'receipt_long'" :size="22" />
      </span>
      <div>
        <h3>{{ formTitle }}</h3>
        <p>{{ helperText }}</p>
      </div>
    </div>

    <form class="compact-form" @submit.prevent="submitForm">
      <label class="full-field">
        <span>Concepto</span>
        <input v-model.trim="form.description" maxlength="255" placeholder="Descripcion" type="text" />
      </label>
      <label class="full-field">
        <span>Categoria</span>
        <select v-model="form.categoryId" required>
          <option value="" disabled>Selecciona categoria</option>
          <option v-for="category in categoryOptions" :key="category.id" :value="String(category.id)">
            {{ category.name }}
          </option>
        </select>
      </label>
      <div class="form-row">
        <label>
          <span>Monto</span>
          <input v-model="form.amount" placeholder="0.00" type="number" min="0.01" step="0.01" required />
        </label>
        <label>
          <span>Fecha</span>
          <input v-model="form.date" type="date" :max="currentDate()" required />
        </label>
      </div>
      <button class="submit-button compact" type="submit" :disabled="isSaving">
        <AppIcon :name="editingTransaction ? 'save' : 'add_circle'" :size="20" />
        {{ editingTransaction ? 'Guardar cambios' : ctaLabel }}
      </button>
      <button
        v-if="editingTransaction"
        class="secondary-action compact-secondary"
        type="button"
        @click="emit('cancel')"
      >
        Cancelar edicion
      </button>
    </form>
  </aside>
</template>

<style scoped>
.quick-form-panel {
  width: 100%;
  padding: 28px;
  border-color: rgba(82, 231, 168, 0.22);
}

.quick-form-panel.expense {
  border-color: rgba(255, 109, 122, 0.22);
}

.quick-form-heading {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 20px;
}

.quick-form-heading h3 {
  font-size: 20px;
  line-height: 1.2;
}

.quick-form-heading p {
  margin-top: 4px;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 700;
}

.form-icon {
  display: grid;
  width: 44px;
  height: 44px;
  flex: 0 0 auto;
  place-items: center;
  border-radius: var(--radius);
  background: var(--secondary-soft);
  color: var(--secondary);
}

.quick-form-panel.expense .form-icon {
  background: var(--danger-soft);
  color: var(--danger);
}

.compact-form {
  display: grid;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.submit-button.compact {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.compact-secondary {
  width: 100%;
}

@media (max-width: 540px) {
  .quick-form-panel {
    padding: 22px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>

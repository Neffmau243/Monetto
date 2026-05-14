<script setup lang="ts">
import { computed, reactive, watch } from 'vue'
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
  <aside class="panel quick-form-panel">
    <div class="panel-heading">
      <div>
        <h3>{{ formTitle }}</h3>
        <p>{{ helperText }}</p>
      </div>
    </div>

    <form class="compact-form" @submit.prevent="submitForm">
      <label>
        <span>Concepto</span>
        <input v-model.trim="form.description" maxlength="255" placeholder="Descripcion" type="text" />
      </label>
      <label>
        <span>Categoria</span>
        <select v-model="form.categoryId" required>
          <option value="" disabled>Selecciona categoria</option>
          <option v-for="category in categoryOptions" :key="category.id" :value="String(category.id)">
            {{ category.name }}
          </option>
        </select>
      </label>
      <label>
        <span>Monto</span>
        <input v-model="form.amount" placeholder="0.00" type="number" min="0.01" step="0.01" required />
      </label>
      <label>
        <span>Fecha</span>
        <input v-model="form.date" type="date" :max="currentDate()" required />
      </label>
      <button class="submit-button compact" type="submit" :disabled="isSaving">
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
  position: sticky;
  top: 100px;
}

.compact-form {
  display: grid;
  gap: 16px;
}

.compact-secondary {
  width: 100%;
}

@media (max-width: 1180px) {
  .quick-form-panel {
    position: static;
  }
}
</style>

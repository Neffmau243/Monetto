<script setup lang="ts">
import { computed, onMounted, reactive, shallowRef } from 'vue'
import AppIcon from '../components/AppIcon.vue'
import { useAuthSession } from '../composables/useAuthSession'
import {
  createCategory,
  deleteCategory,
  getCategories,
  updateCategory,
} from '../services/monettoApi'
import { mapCategory } from '../services/monettoMappers'
import type { Category, TransactionType } from '../types'

const { requireToken } = useAuthSession()
const categories = shallowRef<Category[]>([])
const isLoading = shallowRef(false)
const errorMessage = shallowRef('')
const form = reactive<{
  editingId: number | null
  name: string
  type: TransactionType
}>({
  editingId: null,
  name: '',
  type: 'EXPENSE',
})

const groupedCategories = computed(() => ({
  expense: categories.value.filter((category) => category.type === 'EXPENSE'),
  income: categories.value.filter((category) => category.type === 'INCOME'),
}))

const categoryCounts = computed<Record<Lowercase<TransactionType>, number>>(() => ({
  expense: groupedCategories.value.expense.length,
  income: groupedCategories.value.income.length,
}))

async function loadCategories() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await getCategories(requireToken())
    categories.value = response.map(mapCategory)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudieron cargar categorias'
  } finally {
    isLoading.value = false
  }
}

function startCreate(type: TransactionType) {
  form.editingId = null
  form.name = ''
  form.type = type
}

function startEdit(category: Category) {
  form.editingId = category.id
  form.name = category.name
  form.type = category.type
}

function resetForm() {
  form.editingId = null
  form.name = ''
  form.type = 'EXPENSE'
}

async function submitCategory() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const token = requireToken()
    const payload = { name: form.name, type: form.type }

    if (form.editingId) {
      await updateCategory(token, form.editingId, payload)
    } else {
      await createCategory(token, payload)
    }

    resetForm()
    await loadCategories()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo guardar categoria'
  } finally {
    isLoading.value = false
  }
}

async function removeCategory(category: Category) {
  isLoading.value = true
  errorMessage.value = ''

  try {
    await deleteCategory(requireToken(), category.id)
    await loadCategories()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo eliminar categoria'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  void loadCategories()
})
</script>

<template>
  <section class="page-stack">
    <header class="page-header">
      <div>
        <h2>Gestion de categorias</h2>
        <p>Personaliza como organizas ingresos y gastos sin tocar las categorias default.</p>
      </div>
      <button class="primary-inline-action" type="button" @click="startCreate('EXPENSE')">
        <AppIcon name="add" :size="20" />
        Nueva categoria
      </button>
    </header>

    <p v-if="errorMessage" class="page-error" role="alert">{{ errorMessage }}</p>

    <div class="categories-grid">
      <article class="panel">
        <div class="panel-heading">
          <div>
            <h3>Gastos</h3>
            <p>{{ categoryCounts.expense }} categorias activas</p>
          </div>
          <button class="secondary-action mini-action" type="button" @click="startCreate('EXPENSE')">
            <AppIcon name="add" :size="18" />
            Gasto
          </button>
        </div>

        <div v-if="groupedCategories.expense.length === 0" class="empty-state">
          Sin categorias de gasto registradas.
        </div>
        <div v-else class="category-card-list">
          <div v-for="category in groupedCategories.expense" :key="category.id" class="category-card">
            <div class="category-icon" :style="{ color: category.color }">
              <AppIcon :name="category.icon" :size="23" />
            </div>
            <div>
              <strong>{{ category.name }}</strong>
              <span>{{ category.isDefault ? 'Predeterminada' : 'Personalizada' }}</span>
            </div>
            <div class="row-actions">
              <button
                v-if="!category.isDefault"
                class="icon-button"
                type="button"
                aria-label="Editar categoria"
                @click="startEdit(category)"
              >
                <AppIcon name="edit" :size="18" />
              </button>
              <button
                v-if="!category.isDefault"
                class="icon-button danger"
                type="button"
                aria-label="Eliminar categoria"
                @click="removeCategory(category)"
              >
                <AppIcon name="delete" :size="18" />
              </button>
            </div>
          </div>
        </div>
      </article>

      <article class="panel">
        <div class="panel-heading">
          <div>
            <h3>Ingresos</h3>
            <p>{{ categoryCounts.income }} categorias activas</p>
          </div>
          <button class="secondary-action mini-action" type="button" @click="startCreate('INCOME')">
            <AppIcon name="add" :size="18" />
            Ingreso
          </button>
        </div>

        <div v-if="groupedCategories.income.length === 0" class="empty-state">
          Sin categorias de ingreso registradas.
        </div>
        <div v-else class="category-card-list">
          <div v-for="category in groupedCategories.income" :key="category.id" class="category-card">
            <div class="category-icon" :style="{ color: category.color }">
              <AppIcon :name="category.icon" :size="23" />
            </div>
            <div>
              <strong>{{ category.name }}</strong>
              <span>{{ category.isDefault ? 'Predeterminada' : 'Personalizada' }}</span>
            </div>
            <div class="row-actions">
              <button
                v-if="!category.isDefault"
                class="icon-button"
                type="button"
                aria-label="Editar categoria"
                @click="startEdit(category)"
              >
                <AppIcon name="edit" :size="18" />
              </button>
              <button
                v-if="!category.isDefault"
                class="icon-button danger"
                type="button"
                aria-label="Eliminar categoria"
                @click="removeCategory(category)"
              >
                <AppIcon name="delete" :size="18" />
              </button>
            </div>
          </div>
        </div>
      </article>
    </div>

    <article class="panel">
      <div class="panel-heading">
        <div>
          <h3>{{ form.editingId ? 'Editar categoria' : 'Crear nueva categoria' }}</h3>
          <p>El backend valida nombre unico por usuario y tipo.</p>
        </div>
      </div>
      <form class="category-form" @submit.prevent="submitCategory">
        <label>
          <span>Nombre de la categoria</span>
          <input v-model.trim="form.name" type="text" minlength="2" maxlength="120" required />
        </label>
        <label>
          <span>Tipo de flujo</span>
          <select v-model="form.type">
            <option value="EXPENSE">Gasto</option>
            <option value="INCOME">Ingreso</option>
          </select>
        </label>
        <button class="submit-button compact" type="submit" :disabled="isLoading">
          {{ form.editingId ? 'Guardar cambios' : 'Guardar' }}
        </button>
        <button v-if="form.editingId" class="secondary-action" type="button" @click="resetForm">
          Cancelar
        </button>
      </form>
    </article>
  </section>
</template>

<style scoped>
.mini-action {
  min-height: 38px;
  padding: 0 12px;
}

.page-error {
  padding: 12px 14px;
  border: 1px solid rgba(255, 109, 122, 0.28);
  border-radius: var(--radius);
  background: var(--danger-soft);
  color: var(--danger);
  font-weight: 800;
}
</style>

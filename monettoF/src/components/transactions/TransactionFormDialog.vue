<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '../AppIcon.vue'
import TransactionQuickForm from './TransactionQuickForm.vue'
import type { Category, Transaction, TransactionFormPayload } from '../../types'

const props = defineProps<{
  categoryOptions: Category[]
  ctaLabel: string
  editingTransaction: Transaction | null
  isIncome: boolean
  isOpen: boolean
  isSaving: boolean
}>()

const emit = defineEmits<{
  close: []
  save: [payload: TransactionFormPayload]
}>()

const dialogLabel = computed(() => {
  if (props.editingTransaction) {
    return props.isIncome ? 'Editar ingreso' : 'Editar gasto'
  }

  return props.isIncome ? 'Nuevo ingreso' : 'Nuevo gasto'
})
</script>

<template>
  <Teleport to="body">
    <div v-if="isOpen" class="transaction-dialog-backdrop" @click.self="emit('close')" @keydown.esc="emit('close')">
      <section class="transaction-dialog" role="dialog" aria-modal="true" :aria-label="dialogLabel">
        <button class="dialog-close icon-button" type="button" aria-label="Cerrar formulario" @click="emit('close')">
          <AppIcon name="close" :size="22" />
        </button>

        <TransactionQuickForm
          :category-options="categoryOptions"
          :cta-label="ctaLabel"
          :editing-transaction="editingTransaction"
          :is-income="isIncome"
          :is-saving="isSaving"
          @cancel="emit('close')"
          @save="emit('save', $event)"
        />
      </section>
    </div>
  </Teleport>
</template>

<style scoped>
.transaction-dialog-backdrop {
  position: fixed;
  z-index: 1200;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 24px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.62);
  backdrop-filter: blur(8px);
}

.transaction-dialog {
  position: relative;
  width: min(560px, 100%);
  max-height: calc(100dvh - 48px);
  outline: 0;
}

.dialog-close {
  position: absolute;
  z-index: 2;
  top: 16px;
  right: 16px;
  border: 1px solid var(--outline);
  background: var(--surface);
  color: var(--text);
}

@media (max-width: 560px) {
  .transaction-dialog-backdrop {
    align-items: end;
    padding: 12px;
  }

  .transaction-dialog {
    width: 100%;
    max-height: calc(100dvh - 24px);
  }
}
</style>

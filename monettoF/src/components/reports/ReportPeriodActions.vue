<script setup lang="ts">
import AppIcon from '../AppIcon.vue'

const selectedPeriod = defineModel<string>({ required: true })

const emit = defineEmits<{
  download: []
}>()
</script>

<template>
  <div class="report-actions">
    <label>
      <span>Seleccionar periodo</span>
      <input v-model="selectedPeriod" type="month" />
    </label>
    <button class="primary-inline-action" type="button" @click="emit('download')">
      <AppIcon name="picture_as_pdf" :size="20" />
      Descargar PDF
    </button>
  </div>
</template>

<style scoped>
.report-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.report-actions label {
  min-width: 180px;
}

@media (max-width: 720px) {
  .report-actions {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>

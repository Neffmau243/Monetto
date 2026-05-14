<script setup lang="ts">
import AppIcon from '../AppIcon.vue'

defineProps<{
  ctaLabel: string
  helper: string
  title: string
}>()
</script>

<template>
  <header class="page-header">
    <div>
      <h2>{{ title }}</h2>
      <p>{{ helper }}</p>
    </div>
    <button class="primary-inline-action" type="button">
      <AppIcon name="add_circle" :size="20" />
      {{ ctaLabel }}
    </button>
  </header>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}

.page-header h2 {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.25;
}

.page-header p {
  color: var(--text-muted);
}

@media (max-width: 720px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-header h2 {
    font-size: 28px;
  }
}
</style>

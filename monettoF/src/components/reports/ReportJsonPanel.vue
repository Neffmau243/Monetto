<script setup lang="ts">
defineProps<{
  previewJson: string
}>()
</script>

<template>
  <article class="panel json-panel">
    <div class="panel-heading">
      <div>
        <h3>Previsualización JSON</h3>
        <p>Respuesta esperada del reporte mensual.</p>
      </div>
    </div>
    <pre>{{ previewJson }}</pre>
  </article>
</template>

<style scoped>
.json-panel pre {
  max-height: 230px;
  overflow: auto;
  margin: 0;
  padding: 16px;
  border: 1px solid var(--outline);
  border-radius: var(--radius);
  background: #111917;
  color: #e5f6ef;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 13px;
  line-height: 1.6;
}
</style>

<script setup lang="ts">
withDefaults(
  defineProps<{
    name: string
    label?: string
    size?: number
  }>(),
  {
    size: 24,
  },
)
</script>

<template>
  <span
    class="material-symbols-outlined app-icon"
    :aria-hidden="label ? undefined : true"
    :aria-label="label"
    :style="{ fontSize: `${size}px`, width: `${size}px`, height: `${size}px` }"
  >
    {{ name }}
  </span>
</template>

<style scoped>
.app-icon {
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-variation-settings: 'FILL' 0, 'wght' 430, 'GRAD' 0, 'opsz' 24;
  line-height: 1;
  user-select: none;
}
</style>

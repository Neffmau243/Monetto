<script setup lang="ts">
import AppIcon from '../AppIcon.vue'

defineProps<{
  label: string
  value: string
  icon: string
  tone?: 'neutral' | 'income' | 'expense' | 'success' | 'warning' | 'critical'
  detail?: string
  featured?: boolean
}>()
</script>

<template>
  <article class="stat-card" :class="[tone, { featured }]">
    <div class="stat-card-header">
      <span>{{ label }}</span>
      <span class="stat-icon">
        <AppIcon :name="icon" :size="22" />
      </span>
    </div>
    <strong>{{ value }}</strong>
    <p v-if="detail">{{ detail }}</p>
  </article>
</template>

<style scoped>
.stat-card {
  position: relative;
  overflow: hidden;
  display: grid;
  align-content: space-between;
  min-height: 178px;
  padding: 24px;
  border: 1px solid rgba(51, 215, 218, 0.16);
  border-radius: var(--radius);
  background:
    linear-gradient(180deg, rgba(9, 31, 35, 0.98), rgba(7, 28, 32, 0.98)),
    var(--surface);
  box-shadow: var(--shadow-soft);
}

.stat-card.featured {
  min-height: 210px;
  border-color: rgba(8, 239, 245, 0.34);
  background:
    linear-gradient(135deg, rgba(8, 239, 245, 0.16), rgba(82, 231, 168, 0.08) 52%, rgba(7, 28, 32, 0.98)),
    var(--surface);
}

.stat-card::before {
  position: absolute;
  inset: 0 0 auto;
  height: 3px;
  background: var(--accent);
  content: '';
}

.stat-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
  color: var(--text-muted);
  font-size: 14px;
  font-weight: 800;
}

.stat-icon {
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  border-radius: var(--radius);
  background: var(--accent-soft);
  color: var(--accent);
}

.stat-card strong {
  display: block;
  color: var(--text);
  font-size: 36px;
  line-height: 1.15;
  word-break: break-word;
  font-variant-numeric: tabular-nums;
}

.stat-card.featured strong {
  margin-top: 6px;
  font-size: clamp(42px, 4vw, 58px);
  letter-spacing: 0;
}

.stat-card p {
  margin-top: 12px;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 700;
}

.stat-card.income .stat-card-header {
  color: var(--secondary);
}

.stat-card.income::before {
  background: var(--secondary);
}

.stat-card.income .stat-icon {
  background: var(--secondary-soft);
  color: var(--secondary);
}

.stat-card.expense .stat-card-header {
  color: var(--danger);
}

.stat-card.expense::before {
  background: var(--danger);
}

.stat-card.expense .stat-icon {
  background: var(--danger-soft);
  color: var(--danger);
}

.stat-card.success .stat-card-header,
.stat-card.success:not(.featured) strong {
  color: var(--secondary);
}

.stat-card.success::before {
  background: var(--secondary);
}

.stat-card.success .stat-icon {
  background: var(--secondary-soft);
  color: var(--secondary);
}

.stat-card.warning .stat-card-header,
.stat-card.warning:not(.featured) strong {
  color: var(--warning);
}

.stat-card.warning::before {
  background: var(--warning);
}

.stat-card.warning .stat-icon {
  background: var(--warning-soft);
  color: var(--warning);
}

.stat-card.critical .stat-card-header,
.stat-card.critical:not(.featured) strong {
  color: var(--danger);
}

.stat-card.critical::before {
  background: var(--danger);
}

.stat-card.critical .stat-icon {
  background: var(--danger-soft);
  color: var(--danger);
}

@media (max-width: 720px) {
  .stat-card strong {
    font-size: 32px;
  }
}
</style>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import AppShell from './components/layout/AppShell.vue'
import LoginView from './views/LoginView.vue'
import { useAuthSession } from './composables/useAuthSession'
import type { ViewKey } from './types'

const { clearSession, isAuthenticated, loadCurrentUser, userLabel } = useAuthSession()
const route = useRoute()
const router = useRouter()

const activeView = computed<ViewKey>(() => route.meta.viewKey ?? 'dashboard')

watch(
  () => [isAuthenticated.value, route.name, route.fullPath] as const,
  ([authenticated, routeName, fullPath]) => {
    if (!authenticated && routeName !== 'login') {
      router.replace({ name: 'login', query: { redirect: fullPath } })
      return
    }

    if (authenticated && routeName === 'login') {
      router.replace('/dashboard')
    }
  },
  { immediate: true },
)

onMounted(() => {
  if (isAuthenticated.value) {
    void loadCurrentUser().catch(() => {
      clearSession()
      router.replace({ name: 'login' })
    })
  }
})

function handleAuthenticated() {
  const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/dashboard'
  router.replace(redirect)
}

function handleLogout() {
  clearSession()
  router.replace({ name: 'login' })
}
</script>

<template>
  <LoginView v-if="!isAuthenticated" @authenticated="handleAuthenticated" />
  <AppShell v-else :active-view="activeView" :user-label="userLabel" @logout="handleLogout">
    <RouterView />
  </AppShell>
</template>

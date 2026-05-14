import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import type { ViewKey } from '../types'

declare module 'vue-router' {
  interface RouteMeta {
    viewKey?: ViewKey
  }
}

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('../views/DashboardView.vue'),
    meta: { viewKey: 'dashboard' },
  },
  {
    path: '/income',
    name: 'income',
    component: () => import('../views/IncomeView.vue'),
    meta: { viewKey: 'income' },
  },
  {
    path: '/expenses',
    name: 'expenses',
    component: () => import('../views/ExpensesView.vue'),
    meta: { viewKey: 'expenses' },
  },
  {
    path: '/budget',
    name: 'budget',
    component: () => import('../views/BudgetView.vue'),
    meta: { viewKey: 'budget' },
  },
  {
    path: '/categories',
    name: 'categories',
    component: () => import('../views/CategoriesView.vue'),
    meta: { viewKey: 'categories' },
  },
  {
    path: '/reports',
    name: 'reports',
    component: () => import('../views/ReportsView.vue'),
    meta: { viewKey: 'reports' },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard',
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

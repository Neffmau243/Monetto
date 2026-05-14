import type { BudgetRecord, Category, Transaction, ViewKey } from '../types'

export const navItems: Array<{ key: ViewKey; label: string; icon: string; path: string }> = [
  { key: 'dashboard', label: 'Resumen', icon: 'dashboard', path: '/dashboard' },
  { key: 'income', label: 'Ingresos', icon: 'trending_up', path: '/income' },
  { key: 'expenses', label: 'Gastos', icon: 'trending_down', path: '/expenses' },
  { key: 'budget', label: 'Presupuestos', icon: 'account_balance_wallet', path: '/budget' },
  { key: 'categories', label: 'Categorias', icon: 'category', path: '/categories' },
  { key: 'reports', label: 'Reportes', icon: 'insert_chart', path: '/reports' },
]

export const transactions: Transaction[] = []

export const categories: Category[] = []

export const monthlyTrend: Array<{ month: string; income: number; expenses: number }> = []

export const categoryBreakdown: Array<{
  label: string
  value: number
  percent: number
  color: string
}> = []

export const budgetSnapshot = {
  period: '',
  limit: '0.00',
  spent: '0.00',
  remaining: '0.00',
}

export const budgetHistory: BudgetRecord[] = []

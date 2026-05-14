import type {
  BudgetOut,
  BudgetRecord,
  Category,
  CategoryOut,
  ExpensesByCategoryOut,
  Transaction,
  TransactionOut,
  TransactionType,
} from '../types'
import { currentMonth, moneyString, toNumber } from '../utils/formatters'

const fallbackIncomeIcons = ['payments', 'work', 'savings', 'redeem', 'trending_up']
const fallbackExpenseIcons = ['receipt_long', 'shopping_cart', 'bolt', 'restaurant', 'local_activity']
const colors = ['#08eff5', '#52e7a8', '#ffd166', '#ff6d7a', '#89aeb4', '#33d7da']

const categoryIconByName: Record<string, string> = {
  agua: 'water_drop',
  alimentacion: 'restaurant',
  bonos: 'workspace_premium',
  compras: 'shopping_bag',
  educacion: 'school',
  emergencias: 'emergency',
  entretenimiento: 'stadia_controller',
  freelance: 'laptop_mac',
  internet: 'wifi',
  inversiones: 'trending_up',
  juegos: 'sports_esports',
  luz: 'bolt',
  reembolsos: 'undo',
  regalos: 'redeem',
  salario: 'payments',
  salud: 'health_and_safety',
  salidas: 'local_activity',
  servicios: 'receipt_long',
  suscripciones: 'subscriptions',
  transporte: 'directions_bus',
  ventas: 'storefront',
  vivienda: 'home',
}

function normalizeName(name: string) {
  return name
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
}

function categoryIcon(category: CategoryOut) {
  const normalized = normalizeName(category.name)

  if (categoryIconByName[normalized]) {
    return categoryIconByName[normalized]
  }

  const source = category.type === 'INCOME' ? fallbackIncomeIcons : fallbackExpenseIcons

  return source[category.id % source.length]
}

function categoryColor(id: number, type: TransactionType) {
  if (type === 'EXPENSE') {
    return colors[(id + 2) % colors.length]
  }

  return colors[id % colors.length]
}

export function mapCategory(category: CategoryOut): Category {
  return {
    id: category.id,
    name: category.name,
    type: category.type,
    icon: categoryIcon(category),
    color: categoryColor(category.id, category.type),
    userId: category.user_id,
    isDefault: category.is_default,
    sortOrder: category.sort_order,
    displayOrder: category.display_order,
  }
}

export function mapTransaction(transaction: TransactionOut): Transaction {
  return {
    id: transaction.id,
    type: transaction.type,
    date: transaction.date,
    description: transaction.description,
    category: transaction.category?.name ?? 'Sin categoria',
    categoryId: transaction.category_id,
    amount: transaction.amount,
    createdAt: transaction.created_at,
    status: 'Confirmado',
  }
}

export function mapExpenseBreakdown(item: ExpensesByCategoryOut) {
  return {
    label: item.category_name,
    value: toNumber(item.total),
    percent: toNumber(item.percentage),
    color: categoryColor(item.category_id, 'EXPENSE'),
  }
}

export function mapBudgetRecord(budget: BudgetOut, spent = '0.00'): BudgetRecord {
  const remaining = toNumber(budget.amount) - toNumber(spent)
  const usage = toNumber(budget.amount) > 0 ? (toNumber(spent) / toNumber(budget.amount)) * 100 : 0
  const status = usage >= 100 ? 'Excedido' : usage >= 85 ? 'En riesgo' : 'Saludable'

  return {
    id: budget.id,
    period: budget.month.slice(0, 7),
    month: budget.month,
    limit: moneyString(budget.amount),
    spent: moneyString(spent),
    difference: moneyString(remaining),
    status,
  }
}

export function currentBudgetSnapshot(amount = '0.00', spent = '0.00', remaining?: string) {
  const fallbackRemaining = Math.max(0, toNumber(amount) - toNumber(spent))

  return {
    period: currentMonth(),
    limit: moneyString(amount),
    spent: moneyString(spent),
    remaining: moneyString(remaining ?? fallbackRemaining),
  }
}

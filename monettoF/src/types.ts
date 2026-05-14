export type ViewKey = 'dashboard' | 'income' | 'expenses' | 'budget' | 'categories' | 'reports'

export type TransactionType = 'INCOME' | 'EXPENSE'
export type BudgetSource = 'FIXED' | 'DYNAMIC_INCOME'

export interface UserOut {
  id: number
  name: string
  email: string
  created_at: string
}

export interface TokenOut {
  access_token: string
  token_type: 'bearer'
}

export interface CategoryOut {
  id: number
  name: string
  type: TransactionType
  user_id: number | null
  is_default: boolean
  sort_order: number
  display_order: number
}

export interface Transaction {
  id: number
  type: TransactionType
  date: string
  description: string | null
  category: string
  categoryId: number
  amount: string
  createdAt: string
  status: 'Confirmado' | 'Pendiente'
}

export interface Category {
  id: number
  name: string
  type: TransactionType
  icon: string
  color: string
  userId: number | null
  isDefault: boolean
  sortOrder: number
  displayOrder: number
}

export interface BudgetRecord {
  id: number
  period: string
  month: string
  limit: string
  spent: string
  difference: string
  status: 'Saludable' | 'En riesgo' | 'Excedido'
}

export interface TransactionOut {
  id: number
  type: TransactionType
  amount: string
  description: string | null
  date: string
  category_id: number
  user_id: number
  created_at: string
  category: CategoryOut | null
}

export interface PaginatedTransactionsOut {
  items: TransactionOut[]
  total: number
  page: number
  limit: number
  total_pages: number
  has_next: boolean
  has_previous: boolean
}

export interface BudgetOut {
  id: number
  user_id: number
  month: string
  amount: string
  created_at: string
  updated_at: string
}

export interface BudgetInfoOut {
  amount: string
  spent: string
  percentage: string
  remaining: string
  source: BudgetSource
  is_dynamic: boolean
}

export interface DashboardSummaryOut {
  month: string
  total_income: string
  total_expenses: string
  balance: string
  budget_info: BudgetInfoOut | null
}

export interface ExpensesByCategoryOut {
  category_id: number
  category_name: string
  total: string
  percentage: string
}

export interface MonthlyTrendOut {
  month: string
  income: string
  expenses: string
  balance: string
}

export interface ReportMonthlyOut {
  user: UserOut
  month: string
  summary: DashboardSummaryOut
  transactions: TransactionOut[]
  expenses_by_category: ExpensesByCategoryOut[]
}

export interface TransactionFormPayload {
  type: TransactionType
  amount: string
  description: string | null
  date: string
  category_id: number
}

export interface TransactionFiltersState {
  categoryId: string
  dateFrom: string
  dateTo: string
}

export interface PaginationState {
  total: number
  page: number
  limit: number
  totalPages: number
  hasNext: boolean
  hasPrevious: boolean
}

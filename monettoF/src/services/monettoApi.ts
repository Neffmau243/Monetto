import type {
  BudgetOut,
  CategoryOut,
  DashboardSummaryOut,
  ExpensesByCategoryOut,
  MonthlyTrendOut,
  PaginatedTransactionsOut,
  ReportMonthlyOut,
  TokenOut,
  TransactionFiltersState,
  TransactionFormPayload,
  TransactionOut,
  TransactionType,
  UserOut,
} from '../types'

const API_BASE_URL = import.meta.env.VITE_MONETTO_API_URL ?? 'http://127.0.0.1:8000/api'

export class ApiError extends Error {
  readonly detail: string
  readonly status: number

  constructor(status: number, detail: string) {
    super(detail)
    this.name = 'ApiError'
    this.detail = detail
    this.status = status
  }
}

type QueryValue = string | number | boolean | null | undefined

interface RequestOptions extends Omit<RequestInit, 'body'> {
  body?: unknown
  token?: string
}

function buildQuery(params: Record<string, QueryValue>) {
  const query = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      query.set(key, String(value))
    }
  })

  const serialized = query.toString()

  return serialized ? `?${serialized}` : ''
}

async function readError(response: Response) {
  const contentType = response.headers.get('content-type') ?? ''

  if (contentType.includes('application/json')) {
    const payload = (await response.json().catch(() => null)) as { detail?: unknown } | null

    if (typeof payload?.detail === 'string') {
      return payload.detail
    }

    if (Array.isArray(payload?.detail)) {
      return payload.detail
        .map((item) => (typeof item?.msg === 'string' ? item.msg : 'Error de validacion'))
        .join('. ')
    }
  }

  return `Monetto API error ${response.status}`
}

async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const headers = new Headers(options.headers)

  if (options.body !== undefined) {
    headers.set('Content-Type', 'application/json')
  }

  if (options.token) {
    headers.set('Authorization', `Bearer ${options.token}`)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
    headers,
  })

  if (!response.ok) {
    throw new ApiError(response.status, await readError(response))
  }

  const contentType = response.headers.get('content-type') ?? ''

  if (!contentType.includes('application/json')) {
    return undefined as T
  }

  return response.json() as Promise<T>
}

export function register(payload: { name: string; email: string; password: string }) {
  return apiRequest<UserOut>('/auth/register', {
    method: 'POST',
    body: payload,
  })
}

export function login(payload: { email: string; password: string }) {
  return apiRequest<TokenOut>('/auth/login', {
    method: 'POST',
    body: payload,
  })
}

export function getCurrentUser(token: string) {
  return apiRequest<UserOut>('/auth/me', { token })
}

export function getCategories(token: string, type?: TransactionType) {
  return apiRequest<CategoryOut[]>(`/categories${buildQuery({ type })}`, { token })
}

export function createCategory(
  token: string,
  payload: { name: string; type: TransactionType },
) {
  return apiRequest<CategoryOut>('/categories', {
    method: 'POST',
    body: payload,
    token,
  })
}

export function updateCategory(
  token: string,
  categoryId: number,
  payload: { name?: string; type?: TransactionType },
) {
  return apiRequest<CategoryOut>(`/categories/${categoryId}`, {
    method: 'PUT',
    body: payload,
    token,
  })
}

export function deleteCategory(token: string, categoryId: number) {
  return apiRequest<{ message: string }>(`/categories/${categoryId}`, {
    method: 'DELETE',
    token,
  })
}

export function getTransactions(
  token: string,
  params: Partial<TransactionFiltersState> & {
    type?: TransactionType
    page?: number
    limit?: number
  } = {},
) {
  return apiRequest<PaginatedTransactionsOut>(
    `/transactions${buildQuery({
      type: params.type,
      category_id: params.categoryId,
      date_from: params.dateFrom,
      date_to: params.dateTo,
      page: params.page,
      limit: params.limit,
    })}`,
    { token },
  )
}

export function createTransaction(token: string, payload: TransactionFormPayload) {
  return apiRequest<TransactionOut>('/transactions', {
    method: 'POST',
    body: payload,
    token,
  })
}

export function updateTransaction(
  token: string,
  transactionId: number,
  payload: Partial<TransactionFormPayload>,
) {
  return apiRequest<TransactionOut>(`/transactions/${transactionId}`, {
    method: 'PUT',
    body: payload,
    token,
  })
}

export function deleteTransaction(token: string, transactionId: number) {
  return apiRequest<{ message: string }>(`/transactions/${transactionId}`, {
    method: 'DELETE',
    token,
  })
}

export function getBudgets(token: string) {
  return apiRequest<BudgetOut[]>('/budgets', { token })
}

export function createBudget(token: string, payload: { month: string; amount: string }) {
  return apiRequest<BudgetOut>('/budgets', {
    method: 'POST',
    body: payload,
    token,
  })
}

export function updateBudget(
  token: string,
  budgetId: number,
  payload: { month?: string; amount?: string },
) {
  return apiRequest<BudgetOut>(`/budgets/${budgetId}`, {
    method: 'PUT',
    body: payload,
    token,
  })
}

export function deleteBudget(token: string, budgetId: number) {
  return apiRequest<{ message: string }>(`/budgets/${budgetId}`, {
    method: 'DELETE',
    token,
  })
}

export function getDashboardSummary(token: string, month?: string) {
  return apiRequest<DashboardSummaryOut>(`/dashboard/summary${buildQuery({ month })}`, { token })
}

export function getExpensesByCategory(token: string, month?: string) {
  return apiRequest<ExpensesByCategoryOut[]>(
    `/dashboard/expenses-by-category${buildQuery({ month })}`,
    { token },
  )
}

export function getMonthlyTrend(token: string, months = 6) {
  return apiRequest<MonthlyTrendOut[]>(`/dashboard/monthly-trend${buildQuery({ months })}`, {
    token,
  })
}

export function getMonthlyReportJson(token: string, month: string) {
  return apiRequest<ReportMonthlyOut>(`/reports/monthly${buildQuery({ month, format: 'json' })}`, {
    token,
  })
}

export async function downloadMonthlyReportPdf(token: string, month: string) {
  const response = await fetch(
    `${API_BASE_URL}/reports/monthly${buildQuery({ month, format: 'pdf' })}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  if (!response.ok) {
    throw new ApiError(response.status, await readError(response))
  }

  return response.blob()
}

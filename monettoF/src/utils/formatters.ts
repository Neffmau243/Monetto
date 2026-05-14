import type { TransactionType } from '../types'

export function toNumber(value: string | number) {
  const numericValue = typeof value === 'number' ? value : Number(value)

  return Number.isFinite(numericValue) ? numericValue : 0
}

export function formatMoney(
  amount: string | number,
  sign: 'auto' | 'positive' | 'negative' | 'none' = 'none',
) {
  const value = toNumber(amount)
  const prefix =
    sign === 'positive' || (sign === 'auto' && value > 0)
      ? '+ '
      : sign === 'negative' || (sign === 'auto' && value < 0)
        ? '- '
        : ''

  const formatted = new Intl.NumberFormat('es-CO', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Math.abs(value))

  return `${prefix}$${formatted}`
}

export function formatTransactionAmount(amount: string, type: TransactionType) {
  return formatMoney(amount, type === 'INCOME' ? 'positive' : 'negative')
}

export function formatDate(date: string) {
  return new Intl.DateTimeFormat('es-CO', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${date}T00:00:00`))
}

export function percent(value: number) {
  return `${Math.round(value)}%`
}

export function currentDate() {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

export function currentMonth() {
  return currentDate().slice(0, 7)
}

export function formatMonthLabel(month: string) {
  const [year, monthNumber] = month.split('-').map(Number)

  if (!year || !monthNumber) {
    return month
  }

  return new Intl.DateTimeFormat('es-CO', {
    month: 'short',
    year: 'numeric',
  })
    .format(new Date(year, monthNumber - 1, 1))
    .replace('.', '')
}

export function budgetMonthDate(month: string) {
  return `${month}-01`
}

export function moneyString(value: string | number) {
  return toNumber(value).toFixed(2)
}

export function clampPercent(value: string | number) {
  return Math.max(0, Math.min(100, toNumber(value)))
}

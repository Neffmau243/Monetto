import { computed, shallowRef } from 'vue'
import {
  getCurrentUser,
  login as loginRequest,
  register as registerRequest,
} from '../services/monettoApi'
import type { UserOut } from '../types'

const TOKEN_KEY = 'monetto.accessToken'
const EMAIL_KEY = 'monetto.email'
const NAME_KEY = 'monetto.name'

const token = shallowRef(localStorage.getItem(TOKEN_KEY) ?? '')
const userEmail = shallowRef(localStorage.getItem(EMAIL_KEY) ?? '')
const userName = shallowRef(localStorage.getItem(NAME_KEY) ?? '')

function persistSession(accessToken: string, email: string, name?: string) {
  token.value = accessToken
  userEmail.value = email

  if (name) {
    userName.value = name
    localStorage.setItem(NAME_KEY, name)
  }

  localStorage.setItem(TOKEN_KEY, accessToken)
  localStorage.setItem(EMAIL_KEY, email)
}

function persistUser(user: UserOut) {
  userEmail.value = user.email
  userName.value = user.name
  localStorage.setItem(EMAIL_KEY, user.email)
  localStorage.setItem(NAME_KEY, user.name)
}

function clearSession() {
  token.value = ''
  userEmail.value = ''
  userName.value = ''
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(EMAIL_KEY)
  localStorage.removeItem(NAME_KEY)
}

async function login(email: string, password: string) {
  const response = await loginRequest({ email, password })
  persistSession(response.access_token, email)
  await loadCurrentUser()
}

async function register(name: string, email: string, password: string) {
  const createdUser = await registerRequest({ name, email, password })
  const response = await loginRequest({ email, password })
  persistSession(response.access_token, createdUser.email, createdUser.name)
}

async function loadCurrentUser() {
  if (!token.value) {
    return null
  }

  const user = await getCurrentUser(token.value)
  persistUser(user)

  return user
}

function requireToken() {
  if (!token.value) {
    throw new Error('Authentication token is required')
  }

  return token.value
}

export function useAuthSession() {
  const isAuthenticated = computed(() => Boolean(token.value))
  const userLabel = computed(() => userName.value || 'Usuario Monetto')

  return {
    clearSession,
    isAuthenticated,
    loadCurrentUser,
    login,
    register,
    requireToken,
    token,
    userEmail,
    userLabel,
    userName,
  }
}

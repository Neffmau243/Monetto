<script setup lang="ts">
import { computed, reactive, shallowRef } from 'vue'
import AppIcon from '../components/AppIcon.vue'
import monettoLogo from '../components/ui/Gemini_Generated_Image_90enth90enth90en-removebg-preview.png'
import { useAuthSession } from '../composables/useAuthSession'
import { ApiError } from '../services/monettoApi'

const emit = defineEmits<{
  authenticated: []
}>()

const mode = shallowRef<'login' | 'register'>('login')
const showPassword = shallowRef(false)
const isSubmitting = shallowRef(false)
const errorMessage = shallowRef('')
const form = reactive({
  email: '',
  name: '',
  password: '',
})
const { login, register } = useAuthSession()

const formTitle = computed(() => (mode.value === 'login' ? 'Iniciar sesion' : 'Crear cuenta'))
const formHelper = computed(() =>
  mode.value === 'login' ? 'Entra a tu panel personal.' : 'Crea tu acceso local para Monetto.',
)
const submitLabel = computed(() => (mode.value === 'login' ? 'Acceder al panel' : 'Crear cuenta'))
const passwordAutocomplete = computed(() =>
  mode.value === 'login' ? 'current-password' : 'new-password',
)

async function submitAuth() {
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    if (mode.value === 'register') {
      await register(form.name, form.email, form.password)
    } else {
      await login(form.email, form.password)
    }

    emit('authenticated')
  } catch (error) {
    errorMessage.value =
      error instanceof ApiError ? error.detail : 'No se pudo conectar con Monetto API'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="auth-page">
    <section class="auth-card" aria-label="Acceso Monetto">
      <header class="auth-brand">
        <img :src="monettoLogo" alt="" class="brand-logo" />
        <div>
          <h1>Monetto</h1>
          <p>Gestion de patrimonio</p>
        </div>
      </header>

      <div class="auth-tabs" role="tablist" aria-label="Acceso Monetto">
        <button
          :class="{ active: mode === 'login' }"
          type="button"
          role="tab"
          :aria-selected="mode === 'login'"
          @click="mode = 'login'"
        >
          Iniciar sesion
        </button>
        <button
          :class="{ active: mode === 'register' }"
          type="button"
          role="tab"
          :aria-selected="mode === 'register'"
          @click="mode = 'register'"
        >
          Crear cuenta
        </button>
      </div>

      <form class="auth-form" novalidate @submit.prevent="submitAuth">
        <div class="form-heading">
          <h2>{{ formTitle }}</h2>
          <p>{{ formHelper }}</p>
        </div>

        <label v-if="mode === 'register'" for="auth-name">
          <span>Nombre</span>
          <span class="field-with-icon">
            <AppIcon name="person" :size="20" />
            <input
              id="auth-name"
              v-model.trim="form.name"
              type="text"
              placeholder="Nombre completo"
              autocomplete="name"
              required
            />
          </span>
        </label>

        <label for="auth-email">
          <span>Correo electronico</span>
          <span class="field-with-icon">
            <AppIcon name="mail" :size="20" />
            <input
              id="auth-email"
              v-model.trim="form.email"
              type="email"
              placeholder="ejemplo@monetto.com"
              autocomplete="email"
              required
            />
          </span>
        </label>

        <label for="auth-password">
          <span>Contrasena</span>
          <span class="field-with-icon">
            <AppIcon name="lock" :size="20" />
            <input
              id="auth-password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="********"
              :autocomplete="passwordAutocomplete"
              minlength="8"
              required
            />
            <button
              class="field-button"
              type="button"
              :aria-label="showPassword ? 'Ocultar contrasena' : 'Mostrar contrasena'"
              @click="showPassword = !showPassword"
            >
              <AppIcon :name="showPassword ? 'visibility' : 'visibility_off'" :size="20" />
            </button>
          </span>
        </label>

        <p v-if="errorMessage" class="form-error" role="alert">{{ errorMessage }}</p>

        <button class="submit-button" type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? 'Conectando...' : submitLabel }}
        </button>
      </form>

      <!-- Social login hidden for now: not used in this personal app.
      <div class="auth-divider"><span>O continua con</span></div>
      <div class="social-row">
        <button type="button">Google</button>
        <button type="button">Apple</button>
      </div>
      -->
    </section>
  </main>
</template>

<style scoped>
.auth-page {
  display: grid;
  min-height: 100dvh;
  place-items: center;
  padding: 24px;
  background:
    linear-gradient(180deg, rgba(8, 239, 245, 0.1), transparent 280px),
    linear-gradient(180deg, #06181b 0, #031114 62%, #020c0e 100%),
    var(--background);
}

.auth-card {
  display: grid;
  width: min(480px, 100%);
  gap: 24px;
  padding: 32px;
  border: 1px solid rgba(51, 215, 218, 0.2);
  border-radius: var(--radius);
  background:
    linear-gradient(180deg, rgba(9, 31, 35, 0.98), rgba(7, 28, 32, 0.98)),
    var(--surface);
  box-shadow: var(--shadow);
}

.auth-brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-logo {
  display: block;
  width: 50px;
  height: 50px;
  object-fit: contain;
  filter: drop-shadow(0 0 8px rgba(8, 239, 245, 0.78)) saturate(1.2);
}

.auth-brand h1 {
  color: var(--primary-strong);
  font-size: 28px;
  font-weight: 800;
  line-height: 1.1;
}

.auth-brand p {
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 700;
}

.auth-tabs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  padding: 4px;
  border: 1px solid var(--outline);
  border-radius: var(--radius);
  background: var(--surface-low);
}

.auth-tabs button {
  min-height: 42px;
  padding: 0 10px;
  border: 0;
  border-radius: calc(var(--radius) - 2px);
  background: transparent;
  color: var(--text-muted);
  font-weight: 800;
  transition:
    background 160ms ease,
    color 160ms ease,
    box-shadow 160ms ease;
}

.auth-tabs button.active {
  background: var(--surface);
  color: var(--primary-strong);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.24);
}

.auth-form {
  display: grid;
  gap: 14px;
}

.form-heading {
  display: grid;
  gap: 6px;
}

.form-heading h2 {
  font-size: 30px;
  line-height: 1.12;
}

.form-heading p {
  color: var(--text-muted);
  font-size: 14px;
  font-weight: 700;
}

.field-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.field-with-icon > :deep(.app-icon) {
  position: absolute;
  left: 12px;
  color: var(--outline-strong);
}

.field-with-icon input {
  padding-right: 48px;
  padding-left: 42px;
}

.field-button {
  position: absolute;
  right: 1px;
  display: grid;
  width: 44px;
  height: 44px;
  place-items: center;
  border: 0;
  border-radius: var(--radius);
  background: transparent;
  color: var(--text-muted);
}

.field-button:hover {
  background: var(--surface-high);
  color: var(--primary-strong);
}

.submit-button {
  margin-top: 4px;
  min-height: 50px;
  padding: 0 18px;
  border: 0;
  border-radius: var(--radius);
  background: var(--primary);
  color: var(--on-primary);
  font-weight: 800;
  transition:
    transform 160ms ease,
    background 160ms ease,
    box-shadow 160ms ease;
}

.submit-button:hover {
  background: var(--primary-hover);
  box-shadow: var(--shadow-soft);
}

.submit-button:active {
  transform: scale(0.98);
}

.form-error {
  padding: 10px 12px;
  border: 1px solid rgba(255, 109, 122, 0.28);
  border-radius: var(--radius);
  background: var(--danger-soft);
  color: var(--danger);
  font-size: 13px;
  font-weight: 800;
}

@media (max-width: 560px) {
  .auth-page {
    padding: 16px;
  }

  .auth-card {
    gap: 20px;
    padding: 24px;
  }

  .form-heading h2 {
    font-size: 26px;
  }
}
</style>

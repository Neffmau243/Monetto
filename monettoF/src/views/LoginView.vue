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

const formTitle = computed(() => (mode.value === 'login' ? 'Iniciar sesión' : 'Crear cuenta'))
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
    <section class="auth-card">
      <div class="auth-visual">
        <div class="auth-brand">
          <div class="brand-mark large">
            <img :src="monettoLogo" alt="" class="brand-logo large" />
          </div>
          <h1>Monetto</h1>
        </div>
        <h2>Tu patrimonio, bajo control absoluto y seguridad total.</h2>
        <p>
          Gestiona transacciones, presupuestos y reportes con la precisión que tu libertad
          financiera requiere.
        </p>
        <div class="trust-list">
          <div>
            <AppIcon name="shield" :size="22" />
            <span>Seguridad bancaria</span>
          </div>
          <div>
            <AppIcon name="insights" :size="22" />
            <span>Análisis inteligente</span>
          </div>
        </div>
        <div class="auth-ledger-art" aria-hidden="true">
          <span></span>
          <span></span>
          <span></span>
          <i></i>
        </div>
      </div>

      <div class="auth-form-panel">
        <div class="mobile-brand">
          <img :src="monettoLogo" alt="" class="brand-logo" />
          <strong>Monetto</strong>
        </div>

        <div class="auth-tabs" role="tablist" aria-label="Acceso Monetto">
          <button
            :class="{ active: mode === 'login' }"
            type="button"
            role="tab"
            :aria-selected="mode === 'login'"
            @click="mode = 'login'"
          >
            Iniciar sesión
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
          <h2>{{ formTitle }}</h2>

          <label for="auth-email">
            <span>Correo electrónico</span>
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
            <span>Contraseña</span>
            <span class="field-with-icon">
              <AppIcon name="lock" :size="20" />
              <input
                id="auth-password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                :autocomplete="passwordAutocomplete"
                minlength="8"
                required
              />
              <button
                class="field-button"
                type="button"
                :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                @click="showPassword = !showPassword"
              >
                <AppIcon :name="showPassword ? 'visibility' : 'visibility_off'" :size="20" />
              </button>
            </span>
          </label>

          <label v-if="mode === 'register'" class="auth-extra-field" for="auth-name">
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

          <div class="form-row">
            <label class="check-label">
              <input type="checkbox" />
              <span>Mantener sesión iniciada</span>
            </label>
            <button class="link-button" :class="{ invisible: mode === 'register' }" type="button">
              ¿Olvidaste tu contraseña?
            </button>
          </div>

          <p v-if="errorMessage" class="form-error" role="alert">{{ errorMessage }}</p>

          <button class="submit-button" type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? 'Conectando...' : submitLabel }}
          </button>
        </form>

        <div class="auth-divider"><span>O continúa con</span></div>

        <div class="social-row">
          <button type="button">Google</button>
          <button type="button">Apple</button>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.auth-page {
  display: grid;
  min-height: 100dvh;
  place-items: center;
  padding: 16px;
  background:
    radial-gradient(circle at 18% 12%, rgba(8, 239, 245, 0.22), transparent 34%),
    radial-gradient(circle at 86% 70%, rgba(51, 215, 218, 0.12), transparent 30%),
    linear-gradient(180deg, #06181b 0, #031114 58%, #020c0e 100%),
    var(--background);
}

.auth-card {
  display: grid;
  width: min(1180px, 100%);
  height: min(700px, calc(100dvh - 32px));
  min-height: 620px;
  grid-template-columns: minmax(0, 1fr) minmax(420px, 0.9fr);
  overflow: hidden;
  border: 1px solid var(--outline);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
}

.auth-visual {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
  padding: 56px;
  background:
    linear-gradient(rgba(8, 239, 245, 0.12) 1px, transparent 1px),
    linear-gradient(90deg, rgba(8, 239, 245, 0.12) 1px, transparent 1px),
    linear-gradient(145deg, #092328 0%, #071c20 48%, #041317 100%);
  background-size: 36px 36px;
  color: var(--text);
}

.auth-brand,
.trust-list div {
  display: flex;
  align-items: center;
}

.auth-brand {
  gap: 14px;
  margin-bottom: 36px;
}

.auth-brand h1 {
  color: var(--primary-strong);
  font-size: 34px;
  font-weight: 800;
}

.brand-mark {
  display: inline-flex;
  width: 44px;
  height: 44px;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(8, 239, 245, 0.52);
  border-radius: var(--radius);
  background:
    radial-gradient(circle at 50% 42%, rgba(8, 239, 245, 0.34), rgba(51, 215, 218, 0.14) 42%, transparent 68%),
    #082326;
  color: var(--primary);
  box-shadow:
    0 0 0 4px rgba(8, 239, 245, 0.1),
    0 14px 28px rgba(8, 239, 245, 0.2);
}

.brand-mark.large {
  width: 54px;
  height: 54px;
}

.brand-logo {
  display: block;
  width: 36px;
  height: 36px;
  object-fit: contain;
  filter: drop-shadow(0 0 8px rgba(8, 239, 245, 0.78)) saturate(1.2);
}

.brand-logo.large {
  width: 48px;
  height: 48px;
}

.auth-visual h2 {
  max-width: 520px;
  color: var(--text);
  font-size: 32px;
  line-height: 1.25;
}

.auth-visual p {
  max-width: 460px;
  margin-top: 16px;
  color: var(--text-muted);
}

.trust-list {
  display: grid;
  gap: 14px;
  margin-top: 44px;
}

.trust-list div {
  width: fit-content;
  gap: 12px;
  padding: 10px 12px;
  border: 1px solid rgba(8, 239, 245, 0.22);
  border-radius: var(--radius);
  background: var(--surface);
  color: var(--text);
  font-weight: 700;
  box-shadow: var(--shadow-soft);
}

.auth-ledger-art {
  position: absolute;
  right: 36px;
  bottom: 28px;
  display: grid;
  width: min(280px, 44%);
  gap: 12px;
  padding: 18px;
  border: 1px solid rgba(8, 239, 245, 0.22);
  border-radius: var(--radius);
  background: rgba(3, 17, 20, 0.76);
  box-shadow: var(--shadow-soft);
  pointer-events: none;
}

.auth-ledger-art span {
  display: block;
  height: 12px;
  border-radius: 999px;
  background: rgba(8, 239, 245, 0.16);
}

.auth-ledger-art span:nth-child(1) {
  width: 86%;
}

.auth-ledger-art span:nth-child(2) {
  width: 64%;
  background: rgba(8, 239, 245, 0.62);
}

.auth-ledger-art span:nth-child(3) {
  width: 74%;
}

.auth-ledger-art i {
  display: block;
  width: 100%;
  height: 86px;
  border-radius: var(--radius);
  background:
    linear-gradient(150deg, transparent 0 28%, rgba(8, 239, 245, 0.78) 28% 33%, transparent 33% 100%),
    linear-gradient(18deg, transparent 0 42%, rgba(51, 215, 218, 0.38) 42% 47%, transparent 47% 100%),
    rgba(8, 239, 245, 0.08);
}

.auth-form-panel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow-y: auto;
  padding: 36px 56px;
}

.mobile-brand {
  display: none;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
}

.mobile-brand strong {
  display: block;
  color: var(--primary-strong);
  font-size: 24px;
  font-weight: 800;
  line-height: 1.1;
}

.auth-tabs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin-bottom: 22px;
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

.auth-form h2 {
  font-size: 28px;
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
  padding-left: 42px;
  padding-right: 48px;
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

.form-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.invisible {
  visibility: hidden;
  pointer-events: none;
}

.check-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
  font-size: 13px;
}

.check-label input {
  width: 18px;
  min-height: 18px;
}

.link-button {
  border: 0;
  background: transparent;
  color: var(--primary-strong);
  font-size: 14px;
  font-weight: 800;
}

.submit-button {
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

.auth-divider {
  position: relative;
  margin: 20px 0;
  text-align: center;
}

.auth-divider::before {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 1px;
  background: var(--outline);
  content: '';
}

.auth-divider span {
  position: relative;
  padding: 0 14px;
  background: var(--surface);
  color: var(--text-muted);
  font-size: 13px;
}

.social-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.social-row button {
  min-height: 44px;
  border: 1px solid var(--outline);
  border-radius: var(--radius);
  background: var(--surface);
  color: var(--text);
  font-weight: 800;
}

.social-row button:hover {
  background: var(--surface-high);
}

@media (max-width: 900px) {
  .auth-card {
    height: auto;
    min-height: 0;
    grid-template-columns: 1fr;
  }

  .auth-visual {
    display: none;
  }

  .auth-form-panel {
    padding: 32px 24px;
  }

  .mobile-brand {
    display: flex;
  }
}

@media (max-width: 720px) {
  .form-row {
    flex-direction: column;
    align-items: stretch;
  }

  .social-row {
    grid-template-columns: 1fr;
  }
}
</style>

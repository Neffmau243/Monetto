<script setup lang="ts">
import { computed, shallowRef, watch } from 'vue'
import { RouterLink } from 'vue-router'
import AppIcon from '../AppIcon.vue'
import { navItems } from '../../data/monetto'
import type { ViewKey } from '../../types'
import monettoLogo from '../ui/Gemini_Generated_Image_90enth90enth90en-removebg-preview.png'

const props = defineProps<{
  activeView: ViewKey
  userLabel: string
}>()

const emit = defineEmits<{
  logout: []
}>()

const activeItem = computed(
  () => navItems.find((item) => item.key === props.activeView) ?? navItems[0],
)

const isMobileMenuOpen = shallowRef(false)

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
}

watch(
  () => props.activeView,
  () => {
    closeMobileMenu()
  },
)
</script>

<template>
  <div class="app-shell" @keydown.esc="closeMobileMenu">
    <a class="skip-link" href="#main-content">Saltar al contenido</a>

    <button
      v-show="isMobileMenuOpen"
      class="mobile-menu-scrim"
      type="button"
      aria-label="Cerrar navegación"
      @click="closeMobileMenu"
    ></button>

    <aside id="app-sidebar" class="sidebar" :class="{ 'mobile-open': isMobileMenuOpen }">
      <div class="brand-block">
        <div class="brand-identity">
          <div class="brand-mark">
            <img :src="monettoLogo" alt="" class="brand-logo" />
          </div>
          <div>
            <strong>Monetto</strong>
            <span>Gestión de patrimonio</span>
          </div>
        </div>
        <button class="sidebar-close icon-button" type="button" aria-label="Cerrar navegación" @click="closeMobileMenu">
          <AppIcon name="close" :size="22" />
        </button>
      </div>

      <div class="profile-strip">
        <div class="avatar">{{ props.userLabel.slice(0, 2).toUpperCase() }}</div>
        <div>
          <p>{{ props.userLabel }}</p>
          <span>Cuenta activa</span>
        </div>
      </div>

      <span class="sidebar-section-label">Principal</span>
      <nav class="side-nav" aria-label="Navegación principal">
        <RouterLink
          v-for="item in navItems"
          :key="item.key"
          :to="item.path"
          class="nav-item"
          :class="{ active: item.key === activeView }"
          :aria-current="item.key === activeView ? 'page' : undefined"
          @click="closeMobileMenu"
        >
          <AppIcon :name="item.icon" :size="22" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>

      <RouterLink class="primary-action" to="/expenses" @click="closeMobileMenu">
        <AppIcon name="add" :size="21" />
        <span>Añadir transacción</span>
      </RouterLink>
    </aside>

    <div class="workspace">
      <header class="topbar">
        <button
          class="menu-toggle icon-button"
          type="button"
          aria-controls="app-sidebar"
          :aria-expanded="isMobileMenuOpen"
          :aria-label="isMobileMenuOpen ? 'Cerrar navegación' : 'Abrir navegación'"
          @click="toggleMobileMenu"
        >
          <AppIcon :name="isMobileMenuOpen ? 'close' : 'menu'" :size="24" />
        </button>
        <div class="topbar-title">
          <span class="eyebrow">Monetto</span>
          <h1>{{ activeItem.label }}</h1>
        </div>
        <form class="topbar-search" role="search" @submit.prevent>
          <label class="sr-only" for="workspace-search">Buscar</label>
          <AppIcon name="search" :size="20" />
          <input id="workspace-search" type="search" placeholder="Buscar movimientos, categorías..." />
        </form>
        <div class="topbar-actions">
          <span class="sync-pill">
            <AppIcon name="check_circle" :size="18" />
            En línea
          </span>
          <button class="icon-button" type="button" aria-label="Notificaciones">
            <AppIcon name="notifications" :size="22" />
          </button>
          <button class="icon-button" type="button" aria-label="Ajustes">
            <AppIcon name="settings" :size="22" />
          </button>
          <button class="ghost-button" type="button" @click="emit('logout')">
            Salir
          </button>
        </div>
      </header>

      <main id="main-content" class="content-area">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100dvh;
}

.skip-link {
  position: fixed;
  top: 12px;
  left: 12px;
  z-index: 100;
  transform: translateY(-160%);
  padding: 10px 14px;
  border-radius: var(--radius);
  background: var(--primary);
  color: var(--on-primary);
  font-weight: 800;
  text-decoration: none;
  transition: transform 160ms ease;
}

.skip-link:focus-visible {
  transform: translateY(0);
}

.mobile-menu-scrim {
  position: fixed;
  inset: 0;
  z-index: 24;
  display: none;
  border: 0;
  background: rgba(0, 0, 0, 0.58);
  backdrop-filter: blur(3px);
}

.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 30;
  display: flex;
  width: var(--sidebar-width);
  flex-direction: column;
  gap: 18px;
  padding: 24px 18px;
  border-right: 1px solid rgba(51, 215, 218, 0.16);
  background:
    radial-gradient(circle at 18% 2%, rgba(8, 239, 245, 0.16), transparent 30%),
    linear-gradient(180deg, rgba(8, 27, 31, 0.98), rgba(3, 17, 20, 0.99)),
    var(--surface);
  box-shadow: 18px 0 42px rgba(0, 0, 0, 0.3);
  transition: transform 220ms ease;
}

.brand-block,
.brand-identity,
.profile-strip,
.nav-item,
.primary-action,
.topbar,
.topbar-actions,
.sync-pill,
.topbar-search {
  display: flex;
  align-items: center;
}

.brand-block {
  justify-content: space-between;
  gap: 12px;
  padding: 6px 4px 12px;
}

.brand-identity {
  min-width: 0;
  gap: 12px;
}

.brand-identity strong {
  display: block;
  font-size: 24px;
  font-weight: 800;
  line-height: 1.1;
  color: var(--primary-strong);
}

.brand-identity span {
  display: block;
  margin-top: 2px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 600;
}

.brand-mark {
  display: inline-flex;
  width: 44px;
  height: 44px;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(8, 239, 245, 0.48);
  border-radius: var(--radius);
  background:
    radial-gradient(circle at 50% 42%, rgba(8, 239, 245, 0.34), rgba(51, 215, 218, 0.14) 42%, transparent 68%),
    #082326;
  color: var(--primary);
  box-shadow:
    0 0 0 4px rgba(8, 239, 245, 0.09),
    0 14px 26px rgba(8, 239, 245, 0.18);
}

.brand-logo {
  display: block;
  width: 36px;
  height: 36px;
  object-fit: contain;
  filter: drop-shadow(0 0 7px rgba(8, 239, 245, 0.72)) saturate(1.18);
}

.sidebar-close,
.menu-toggle {
  display: none;
}

.profile-strip {
  gap: 12px;
  padding: 12px;
  border: 1px solid rgba(51, 215, 218, 0.18);
  border-radius: var(--radius);
  background: var(--surface-low);
}

.profile-strip p {
  font-weight: 700;
}

.profile-strip span {
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
}

.avatar {
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--brand-cyan), var(--brand-aqua));
  color: var(--on-primary);
  font-size: 13px;
  font-weight: 800;
}

.sidebar-section-label {
  padding: 0 12px;
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.side-nav {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  position: relative;
  min-height: 48px;
  gap: 12px;
  width: 100%;
  padding: 12px 14px;
  border-radius: var(--radius);
  color: var(--text-muted);
  font-size: 14px;
  font-weight: 700;
  text-align: left;
  text-decoration: none;
  transition:
    transform 180ms ease,
    background 180ms ease,
    color 180ms ease;
}

.nav-item::before {
  position: absolute;
  top: 11px;
  bottom: 11px;
  left: 6px;
  width: 3px;
  border-radius: 999px;
  background: transparent;
  content: '';
}

.nav-item:hover {
  transform: translateX(3px);
  background: var(--surface-high);
  color: var(--text);
}

.nav-item.active {
  background: var(--primary-soft);
  color: var(--primary-strong);
}

.nav-item.active::before {
  background: var(--primary);
}

.primary-action {
  min-height: 48px;
  justify-content: center;
  gap: 8px;
  width: 100%;
  border-radius: var(--radius);
  background: var(--primary);
  color: var(--on-primary);
  font-weight: 800;
  text-decoration: none;
  transition:
    transform 160ms ease,
    background 160ms ease,
    box-shadow 160ms ease;
}

.primary-action:hover {
  background: var(--primary-hover);
  box-shadow: 0 12px 26px rgba(8, 239, 245, 0.26);
}

.primary-action:active {
  transform: scale(0.98);
}

.workspace {
  min-height: 100dvh;
  margin-left: var(--sidebar-width);
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 12;
  display: grid;
  grid-template-columns: minmax(160px, auto) minmax(280px, 520px) auto;
  justify-content: space-between;
  gap: 18px;
  min-height: 78px;
  padding: 14px 40px;
  border-bottom: 1px solid rgba(51, 215, 218, 0.16);
  background: rgba(3, 17, 20, 0.88);
  backdrop-filter: blur(16px);
}

.topbar-title {
  min-width: 0;
}

.eyebrow {
  display: block;
  color: var(--primary-strong);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.topbar h1 {
  font-size: 24px;
  line-height: 1.2;
}

.topbar-search {
  min-width: 0;
  gap: 10px;
  height: 46px;
  padding: 0 14px;
  border: 1px solid rgba(51, 215, 218, 0.18);
  border-radius: var(--radius);
  background: rgba(7, 28, 32, 0.82);
  color: var(--text-muted);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.topbar-search input {
  min-height: 0;
  padding: 0;
  border: 0;
  background: transparent;
  box-shadow: none;
}

.topbar-search input:focus {
  box-shadow: none;
}

.topbar-actions {
  gap: 10px;
  justify-content: flex-end;
}

.sync-pill {
  min-height: 36px;
  gap: 7px;
  padding: 0 10px;
  border-radius: 999px;
  background: var(--secondary-soft);
  color: var(--secondary);
  font-size: 12px;
  font-weight: 800;
  white-space: nowrap;
}

.ghost-button {
  border: 0;
  background: transparent;
  color: var(--primary-strong);
  font-size: 14px;
  font-weight: 800;
}

.content-area {
  width: min(100%, 1360px);
  margin: 0 auto;
  padding: 32px 40px 64px;
}

@media (max-width: 900px) {
  .sidebar {
    width: min(86vw, 320px);
    transform: translateX(-104%);
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }

  .mobile-menu-scrim {
    display: block;
  }

  .sidebar-close,
  .menu-toggle {
    display: inline-grid;
  }

  .workspace {
    margin-left: 0;
  }

  .topbar {
    grid-template-columns: auto minmax(0, 1fr) auto;
    justify-content: stretch;
    gap: 10px;
    padding: 12px 16px;
  }

  .topbar-search,
  .sync-pill {
    display: none;
  }

  .content-area {
    padding: 24px 16px 40px;
  }
}

@media (max-width: 720px) {
  .topbar-actions .ghost-button {
    display: none;
  }
}
</style>

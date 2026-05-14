<template>
  <header>
    <div class="container">
      <nav class="nav">

        <div class="brand">
          <img src="/img/openart-image_DsdbMeYk_1740823153253_raw.jpg" alt="django" class="brand-img" />
          <div class="logo">django</div>
        </div>

        <ul class="nav-links">
          <li><RouterLink to="/"      class="nav-link" active-class="active">Главная</RouterLink></li>
          <li><RouterLink to="/forum" class="nav-link" active-class="active">Форум</RouterLink></li>
          <li><RouterLink to="/docs"  class="nav-link" active-class="active">Документация</RouterLink></li>
        </ul>

        <div class="auth-buttons">
          <template v-if="auth.isAuthenticated">
            <span class="auth-username">
              <i class="ti ti-user" aria-hidden="true"></i>
              {{ auth.username }}
            </span>
            <RouterLink to="/profile" class="auth-username">
              <img v-if="auth.avatar" :src="auth.avatar" class="brand-img" />
              <span v-else class="avatar-placeholder">{{ auth.username?.slice(0,2).toUpperCase() }}</span>
              {{ auth.nickname || auth.username }}
            </RouterLink>
            <button class="btn btn-logout" @click="handleLogout">
              <i class="ti ti-logout" aria-hidden="true"></i> Выйти
            </button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="btn btn-login">
              <i class="ti ti-login" aria-hidden="true"></i>
              Войти
            </RouterLink>
            <RouterLink to="/register" class="btn btn-register">
              <i class="ti ti-user-plus" aria-hidden="true"></i>
              Регистрация
            </RouterLink>
          </template>
        </div>

      </nav>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth   = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #c8d8a0;
  flex-shrink: 0;
}

.auth-username {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: inherit;
  color: #555;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: inherit;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  border: 1px solid transparent;
  transition: background 0.15s, border-color 0.15s;
}

.btn-login {
  background: transparent;
  color: #3a6e28;
  border-color: #3a6e28;
}

.btn-login:hover {
  background: #e0edcc;
}

.btn-register {
  background: #3a6e28;
  color: #f5f8e9;
  border-color: #2d5520;
}

.btn-register:hover {
  background: #2d5520;
}

.btn-logout {
  background: transparent;
  color: #8b2e2e;
  border-color: #8b2e2e;
}

.btn-logout:hover {
  background: #f7e0e0;
}
</style>
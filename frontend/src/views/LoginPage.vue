<template>
  <div class="login-wrap">
    <div class="login-card">
      <div class="login-logo">django</div>
      <div class="login-sub">Sign in to your account</div>

      <div class="form-field">
        <label class="form-label">Username</label>
        <input v-model="form.username" class="form-input" type="text" placeholder="Enter username" @keyup.enter="handleLogin" />
      </div>
      <div class="form-field">
        <label class="form-label">Password</label>
        <input v-model="form.password" class="form-input" type="password" placeholder="••••••••" @keyup.enter="handleLogin" />
      </div>

      <p v-if="error" class="error-msg">{{ error }}</p>

      <button class="form-btn" :disabled="loading" @click="handleLogin">
        <i class="ti ti-login" aria-hidden="true"></i>
        {{ loading ? 'Signing in...' : 'Sign in' }}
      </button>

      <div class="divider" />
      <div class="login-link">
        No account? <RouterLink to="/register">Register</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'

const auth    = useAuthStore()
const router  = useRouter()
const route   = useRoute()
const loading = ref(false)
const error   = ref('')
const form    = ref({ username: '', password: '' })

async function handleLogin() {
  error.value = ''
  if (!form.value.username || !form.value.password) {
    error.value = 'Please fill in all fields'
    return
  }
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    router.push(route.query.redirect || '/')
  } catch {
    error.value = 'Invalid username or password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap { min-height: 80vh; display: flex; align-items: center; justify-content: center; }
.login-card { background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: var(--border-radius-lg); padding: 2rem; width: 100%; max-width: 360px; }
.login-logo { font-size: 20px; font-weight: 500; margin-bottom: 4px; }
.login-sub { font-size: 14px; color: var(--color-text-secondary); margin-bottom: 1.5rem; }
.form-field { margin-bottom: 14px; }
.form-label { font-size: 13px; color: var(--color-text-secondary); display: block; margin-bottom: 5px; }
.form-input { width: 100%; padding: 8px 12px; border-radius: var(--border-radius-md); border: 0.5px solid var(--color-border-secondary); background: var(--color-background-secondary); color: var(--color-text-primary); font-size: 14px; }
.form-btn { width: 100%; padding: 9px; border-radius: var(--border-radius-md); background: #185FA5; color: #B5D4F4; border: 0.5px solid #0C447C; font-size: 14px; font-weight: 500; cursor: pointer; margin-top: 4px; display: flex; align-items: center; justify-content: center; gap: 6px; }
.form-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.error-msg { font-size: 13px; color: #A32D2D; margin-bottom: 10px; }
.divider { height: 0.5px; background: var(--color-border-tertiary); margin: 1.5rem 0; }
.login-link { font-size: 13px; color: var(--color-text-secondary); text-align: center; }
.login-link a { color: #185FA5; text-decoration: none; }
</style>
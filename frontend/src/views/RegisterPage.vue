<template>
  <div class="container" style="max-width: 400px; margin-top: 60px;">
    <h2>Регистрация</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label>Имя пользователя:</label>
        <input v-model="form.username" class="form-control" placeholder="Введите имя пользователя" />
      </div>
      <div class="form-group">
        <label>Пароль:</label>
        <input v-model="form.password" type="password" class="form-control" placeholder="Введите пароль" />
      </div>
      <div class="form-group">
        <label>Подтвердите пароль:</label>
        <input v-model="form.password2" type="password" class="form-control" placeholder="Повторите пароль" />
      </div>

      <p v-if="error" style="color: red;">{{ error }}</p>

      <div class="form-actions">
        <button type="submit" class="submit-btn">Зарегистрироваться</button>
      </div>

      <p style="margin-top: 16px;">
        Уже есть аккаунт?
        <RouterLink to="/login">Войти</RouterLink>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth   = useAuthStore()
const router = useRouter()
const error  = ref('')

const form = ref({
  username:  '',
  password:  '',
  password2: '',
})

async function handleRegister() {
  error.value = ''

  if (!form.value.username || !form.value.password) {
    error.value = 'Заполните все поля'
    return
  }
  if (form.value.password !== form.value.password2) {
    error.value = 'Пароли не совпадают'
    return
  }

  try {
    await auth.register(form.value.username, form.value.password)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка регистрации'
  }
}
</script>
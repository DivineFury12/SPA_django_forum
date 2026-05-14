import { defineStore } from 'pinia'
import { login, register } from '@/api/auth'
import api from '@/api/index'

function parseJwt(token) {
  const base64 = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
  return JSON.parse(atob(base64))
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    username:    localStorage.getItem('username') || null,
    accessToken: localStorage.getItem('access_token') || null,
    isStaff:     localStorage.getItem('is_staff') === 'true',
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async login(username, password) {
      const { data } = await login(username, password)
      const payload = parseJwt(data.access)
      this.accessToken = data.access
      this.username    = payload.username
      this.isStaff     = payload.is_staff
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      localStorage.setItem('username', payload.username)
      localStorage.setItem('is_staff', payload.is_staff)
    },

    async register(username, password) {
      await register(username, password)
      await this.login(username, password)
    },

    async logout() {
      try {
        // Get CSRF token from cookie so Django accepts the POST
        const csrf = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          ?.split('=')[1]

        // Clear Django session
        await api.post('/users/logout/', {}, {
          headers: { 'X-CSRFToken': csrf },
          withCredentials: true,   // ← sends the sessionid cookie
        })
      } catch {
        // fail silently — JWT cleanup still happens below
      }

      this.accessToken = null
      this.username    = null
      this.isStaff     = false
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('username')
      localStorage.removeItem('is_staff')
    },
  },
})
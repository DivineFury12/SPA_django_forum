import { defineStore } from 'pinia'
import { login, register } from '@/api/auth'
import api from '@/api/index'
import { getProfile } from '@/api/profile'

function parseJwt(token) {
  const base64 = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
  return JSON.parse(atob(base64))
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
  username:    localStorage.getItem('username')    || null,
  accessToken: localStorage.getItem('access_token') || null,
  isStaff:     localStorage.getItem('is_staff') === 'true',
  nickname:    localStorage.getItem('nickname')    || null,
  avatar:      localStorage.getItem('avatar')      || null,
}),



  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async login(username, password) {
      try {
        const { data } = await login(username, password)
        const payload  = parseJwt(data.access)

        this.accessToken = data.access
        this.username    = payload.username
        this.isStaff     = payload.is_staff

        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        localStorage.setItem('username', payload.username)
        localStorage.setItem('is_staff', payload.is_staff)

        await this.fetchProfile()
      } catch (e) {
        console.error('Login error:', e)
        console.error('Response:', e.response?.data)
        throw e
  }

    },

    async fetchProfile() {
      try {
        const { data } = await getProfile()
        console.log('fetchProfile response:', data)
        this.nickname = data.nickname
        this.avatar   = data.avatar
        localStorage.setItem('nickname', data.nickname || '')
        localStorage.setItem('avatar',   data.avatar   || '')
      } catch (e) {
        console.error('fetchProfile failed:')
        console.error('message:', e.message)
        console.error('status:', e.response?.status)
        console.error('data:', e.response?.data)
        console.error('full error:', e)
      }
    },

    async register(username, password) {
      await register(username, password)
      await this.login(username, password)
    },

    async logout() {
      try {
        const csrf = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          ?.split('=')[1]

        await api.post('/users/logout/', {}, {
          headers: { 'X-CSRFToken': csrf },
          withCredentials: true,
        })
      } catch {
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
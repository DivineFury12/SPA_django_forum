import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import HomePage from '@/views/HomePage.vue'
import ForumPage from '@/views/ForumPage.vue'
import DocsPage from '@/views/DocsPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/forum', component: ForumPage },
  { path: '/docs', component: DocsPage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },

  { path: '/docs', component: DocsPage, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
})

export default router
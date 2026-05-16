<template>
  <section class="forum-container">
    <div class="container">
      <div class="forum-header">
        <h2>Темы обсуждения</h2>

        <button
          v-if="auth.isAuthenticated"
          class="new-topic-btn"
          @click="showForm = !showForm"
        >
          Создать новую тему
        </button>
      </div>

      <TopicForm
        v-if="showForm"
        @created="handleCreated"
      />

      <p v-if="!auth.isAuthenticated">
        <RouterLink to="/login">Войдите</RouterLink>,
        чтобы создавать темы.
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import TopicForm from '@/components/TopicForm.vue'

const auth = useAuthStore()
const router = useRouter()

const showForm = ref(false)

function handleCreated() {
  showForm.value = false
  router.push('/docs')
}
</script>
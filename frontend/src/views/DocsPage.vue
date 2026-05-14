<template>
  <section class="forum-container">
    <div class="container">
      <div class="forum-header">
        <h2>Посты</h2>
      </div>

      <div v-if="loading" style="color: var(--color-text-secondary); font-size: 14px;">Загрузка...</div>
      <div v-else-if="posts.length === 0" style="color: var(--color-text-secondary); font-size: 14px;">Постов пока нет.</div>
      <PostCard
        v-else
        v-for="post in posts"
        :key="post.id"
        :post="post"
        @deleted="loadPosts"
        @updated="loadPosts"
      />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAllPosts } from '@/api/posts'
import PostCard from '@/components/PostCard.vue'

const posts   = ref([])
const loading = ref(false)

async function loadPosts() {
  loading.value = true
  try {
    const { data } = await getAllPosts()
    posts.value = data
  } finally {
    loading.value = false
  }
}

onMounted(loadPosts)
</script>
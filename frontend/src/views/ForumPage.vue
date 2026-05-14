<template>
  <section class="forum-container">
    <div class="container">
      <div class="forum-header">
        <h2>Темы обсуждения</h2>
        <button v-if="auth.isAuthenticated" class="new-topic-btn" @click="showForm = !showForm">
          Создать новую тему
        </button>
      </div>

      <div v-if="showForm" class="topic-form">
        <div class="form-group">
          <label>Заголовок темы:</label>
          <input v-model="form.name" class="form-control" placeholder="Введите заголовок" />
        </div>
        <div class="form-group">
          <label>Содержание:</label>
          <textarea v-model="form.description" class="form-control" rows="5" />
        </div>
        <div class="form-group">
          <label>Код (.py файл):</label>
          <input type="file" accept=".py" class="form-control" @change="handleFile" />
        </div>
        <div class="form-group">
          <label>Теги:</label>
          <div v-if="tags.length" class="tags-selector">
            <label
              v-for="tag in tags"
              :key="tag.id"
              class="tag-option"
              :class="{ selected: selectedTags.includes(tag.id) }"
            >
              <input
                type="checkbox"
                :value="tag.id"
                v-model="selectedTags"
                style="display: none;"
              />
              {{ tag.name }}
            </label>
          </div>
          <span v-else style="font-size: 13px; color: #888;">Нет доступных тегов</span>
        </div>

        <p v-if="error" style="color: red;">{{ error }}</p>
        <div class="form-actions">
          <button class="submit-btn" @click="handleCreate">Опубликовать</button>
          <button class="cancel-btn" @click="resetForm">Отмена</button>
        </div>
      </div>

      <p v-if="!auth.isAuthenticated">
        <RouterLink to="/login">Войдите</RouterLink>, чтобы создавать темы.
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createPost, getAllTags } from '@/api/posts'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth         = useAuthStore()
const router       = useRouter()
const showForm     = ref(false)
const error        = ref('')
const form         = ref({ name: '', description: '' })
const codeFile     = ref(null)
const tags         = ref([])
const selectedTags = ref([])

async function loadTags() {
  try {
    const { data } = await getAllTags()
    tags.value = data
  } catch {
    // tags are optional, fail silently
  }
}

function handleFile(e) {
  const file = e.target.files[0]
  if (file && !file.name.endsWith('.py')) {
    error.value = 'Разрешены только .py файлы'
    codeFile.value = null
  } else {
    error.value = ''
    codeFile.value = file
  }
}

function resetForm() {
  form.value = { name: '', description: '' }
  codeFile.value = null
  selectedTags.value = []
  error.value = ''
  showForm.value = false
}

async function handleCreate() {
  if (!form.value.name || !form.value.description) {
    error.value = 'Заполните все поля'
    return
  }
  const formData = new FormData()
  formData.append('name', form.value.name)
  formData.append('description', form.value.description)
  if (codeFile.value) formData.append('code', codeFile.value)
  selectedTags.value.forEach(id => formData.append('tag_ids', id))  // ← append each tag

  try {
    await createPost(formData)
    resetForm()
    router.push('/docs')
  } catch {
    error.value = 'Ошибка при создании поста'
  }
}

onMounted(loadTags)
</script>

<style scoped>
.tags-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}

.tag-option {
  padding: 4px 12px;
  border-radius: var(--border-radius-md, 8px);
  border: 0.5px solid var(--color-border-secondary);
  font-size: 13px;
  cursor: pointer;
  background: var(--color-background-secondary);
  color: var(--color-text-secondary);
  user-select: none;
  transition: all 0.15s;
}

.tag-option.selected {
  background: #E6F1FB;
  color: #0C447C;
  border-color: #185FA5;
}
</style>
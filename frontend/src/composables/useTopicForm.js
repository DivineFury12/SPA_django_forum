import { ref, onMounted } from 'vue'

import {
  createPost,
  getAllTags,
} from '@/api/posts'

export function useTopicForm(onCreated) {
  const form = ref({
    name: '',
    description: '',
  })

  const codeFile = ref(null)
  const tags = ref([])
  const selectedTags = ref([])
  const error = ref('')

  async function loadTags() {
    try {
      const { data } = await getAllTags()
      tags.value = data
    } catch {
      tags.value = []
    }
  }

  function handleFile(event) {
    const file = event.target.files[0]

    if (file && !file.name.endsWith('.py')) {
      error.value = 'Разрешены только .py файлы'
      codeFile.value = null

      return
    }

    error.value = ''
    codeFile.value = file
  }

  function resetForm() {
    form.value = {
      name: '',
      description: '',
    }

    codeFile.value = null
    selectedTags.value = []
    error.value = ''
  }

  async function submit() {
    if (!form.value.name || !form.value.description) {
      error.value = 'Заполните все поля'
      return
    }

    const formData = new FormData()

    formData.append('name', form.value.name)
    formData.append('description', form.value.description)

    if (codeFile.value) {
      formData.append('code', codeFile.value)
    }

    selectedTags.value.forEach(id => {
      formData.append('tag_ids', id)
    })

    try {
      await createPost(formData)

      resetForm()

      if (onCreated) {
        onCreated()
      }
    } catch {
      error.value = 'Ошибка при создании поста'
    }
  }

  onMounted(loadTags)

  return {
    form,
    tags,
    selectedTags,
    error,
    handleFile,
    resetForm,
    submit,
  }
}
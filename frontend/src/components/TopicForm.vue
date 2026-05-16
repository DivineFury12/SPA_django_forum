<template>
  <div class="topic-form">
    <div class="form-group">
      <label>Заголовок темы:</label>

      <input
        v-model="form.name"
        class="form-control"
        placeholder="Введите заголовок"
      />
    </div>

    <div class="form-group">
      <label>Содержание:</label>

      <textarea
        v-model="form.description"
        class="form-control"
        rows="5"
      />
    </div>

    <div class="form-group">
      <label>Код (.py файл):</label>

      <input
        type="file"
        accept=".py"
        class="form-control"
        @change="handleFile"
      />
    </div>

    <div class="form-group">
      <label>Теги:</label>

      <TagSelector
        :tags="tags"
        v-model="selectedTags"
      />
    </div>

    <p v-if="error" class="error-text">
      {{ error }}
    </p>

    <div class="form-actions">
      <button
        class="submit-btn"
        @click="submit"
      >
        Опубликовать
      </button>

      <button
        class="cancel-btn"
        @click="resetForm"
      >
        Отмена
      </button>
    </div>
  </div>
</template>

<script setup>
import TagSelector from './TagSelector.vue'
import { useTopicForm } from '@/composables/useTopicForm'

const emit = defineEmits(['created'])

const {
  form,
  tags,
  selectedTags,
  error,
  handleFile,
  resetForm,
  submit,
} = useTopicForm(() => {
  emit('created')
})
</script>

<style scoped>
.error-text {
  color: red;
}
</style>
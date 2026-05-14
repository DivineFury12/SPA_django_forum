<template>
  <div class="post-card">
    <template v-if="!editing">
      <div class="post-header">
        <h3 class="post-title">{{ post.name }}</h3>
      </div>

      <div class="post-meta">
        <div class="avatar">{{ initials }}</div>
        <span class="author">{{ post.author }}</span>
        <span class="date">· {{ formatDate(post.created_at) }}</span>
      </div>

      <div v-if="post.tags?.length" class="tags">
        <span v-for="tag in post.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
      </div>

      <p class="post-desc">{{ post.description }}</p>

      <div class="post-footer">
        <a v-if="post.code" :href="post.code" target="_blank" class="file-link">
          <i class="ti ti-file" aria-hidden="true"></i> {{ fileName(post.code) }}
        </a>
        <span v-else />

        <div v-if="canModify" class="btn-row">
          <button class="btn btn-warning btn-sm" @click="editing = true">
            <i class="ti ti-edit" aria-hidden="true"></i> Edit
          </button>
          <button class="btn btn-danger btn-sm" @click="handleDelete">
            <i class="ti ti-trash" aria-hidden="true"></i> Delete
          </button>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="form-field">
        <label class="form-label">Title</label>
        <input v-model="editForm.name" class="form-input" />
      </div>
      <div class="form-field">
        <label class="form-label">Description</label>
        <textarea v-model="editForm.description" class="form-input" rows="4" />
      </div>
      <p v-if="error" class="error-msg">{{ error }}</p>
      <div class="btn-row">
        <button class="btn btn-primary btn-sm" @click="handleUpdate">
          <i class="ti ti-check" aria-hidden="true"></i> Save
        </button>
        <button class="btn btn-ghost btn-sm" @click="editing = false">
          <i class="ti ti-x" aria-hidden="true"></i> Cancel
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { updatePost, deletePost } from '@/api/posts'
import { useAuthStore } from '@/stores/auth'

const props = defineProps(['post'])
const emit  = defineEmits(['deleted', 'updated'])

const auth     = useAuthStore()
const editing  = ref(false)
const error    = ref('')
const editForm = ref({ name: props.post.name, description: props.post.description })

const initials = computed(() =>
  props.post.author?.slice(0, 2).toUpperCase()
)

const canModify = computed(() =>
  auth.isAuthenticated && (auth.username === props.post.author || auth.isStaff)
)

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}

function fileName(url) {
  return url?.split('/').pop() || 'file.py'
}

async function handleDelete() {
  if (!confirm('Delete this post?')) return
  await deletePost(props.post.id)
  emit('deleted')
}

async function handleUpdate() {
  error.value = ''
  try {
    await updatePost(props.post.id, {
      name: editForm.value.name,
      description: editForm.value.description,
    })
    editing.value = false
    emit('updated')
  } catch {
    error.value = 'Failed to update post'
  }
}
</script>

<style scoped>
.post-card { background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: var(--border-radius-lg); padding: 1.25rem; margin-bottom: 1rem; }
.post-header { margin-bottom: 10px; }
.post-title { font-size: 16px; font-weight: 500; }
.post-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.avatar { width: 26px; height: 26px; border-radius: 50%; background: #B5D4F4; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 500; color: #0C447C; flex-shrink: 0; }
.author { font-size: 13px; color: var(--color-text-secondary); }
.date { font-size: 12px; color: var(--color-text-tertiary); }
.tags { display: flex; gap: 5px; flex-wrap: wrap; margin-bottom: 10px; }
.tag { background: #E6F1FB; color: #0C447C; font-size: 11px; padding: 2px 8px; border-radius: var(--border-radius-md); }
.post-desc { font-size: 14px; color: var(--color-text-secondary); line-height: 1.6; margin-bottom: 14px; }
.post-footer { display: flex; justify-content: space-between; align-items: center; border-top: 0.5px solid var(--color-border-tertiary); padding-top: 12px; }
.file-link { display: inline-flex; align-items: center; gap: 5px; font-size: 13px; color: #185FA5; text-decoration: none; }
.btn-row { display: flex; gap: 8px; }
.btn { display: inline-flex; align-items: center; gap: 5px; border-radius: var(--border-radius-md); font-size: 14px; font-weight: 500; cursor: pointer; border: 0.5px solid transparent; }
.btn-sm { padding: 5px 12px; font-size: 13px; }
.btn-primary { background: #185FA5; color: #B5D4F4; border-color: #0C447C; }
.btn-warning { background: #854F0B; color: #FAC775; border-color: #633806; }
.btn-danger { background: #A32D2D; color: #F7C1C1; border-color: #791F1F; }
.btn-ghost { background: var(--color-background-secondary); color: var(--color-text-primary); border-color: var(--color-border-secondary); }
.form-field { margin-bottom: 12px; }
.form-label { font-size: 13px; color: var(--color-text-secondary); display: block; margin-bottom: 5px; }
.form-input { width: 100%; padding: 8px 12px; border-radius: var(--border-radius-md); border: 0.5px solid var(--color-border-secondary); background: var(--color-background-secondary); color: var(--color-text-primary); font-size: 14px; }
.error-msg { font-size: 13px; color: #A32D2D; margin-bottom: 10px; }
</style>
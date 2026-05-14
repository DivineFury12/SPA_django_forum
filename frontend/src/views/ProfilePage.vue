<!-- src/views/ProfilePage.vue -->
<template>
  <div class="container" style="max-width: 480px; margin-top: 40px;">
    <h2 style="margin-bottom: 1.5rem;">Профиль</h2>

    <div class="profile-avatar-row">
      <img v-if="preview || auth.avatar" :src="preview || auth.avatar" class="profile-avatar" />
      <div v-else class="profile-avatar-placeholder">{{ initials }}</div>
      <label class="btn-upload">
        <i class="ti ti-camera" aria-hidden="true"></i> Сменить фото
        <input type="file" accept="image/*" style="display:none" @change="handleAvatar" />
      </label>
    </div>

    <div class="form-group" style="margin-top: 1.5rem;">
      <label class="form-label">Никнейм</label>
      <input v-model="form.nickname" class="form-control" placeholder="Введите никнейм" />
    </div>

    <p v-if="error"   style="color: red;   font-size: 13px; margin-top: 8px;">{{ error }}</p>
    <p v-if="success" style="color: green; font-size: 13px; margin-top: 8px;">Сохранено!</p>

    <div class="form-actions" style="margin-top: 1rem;">
      <button class="submit-btn" @click="handleSave">Сохранить</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { updateProfile } from '@/api/profile'
import { useAuthStore } from '@/stores/auth'

const auth    = useAuthStore()
const error   = ref('')
const success = ref(false)
const preview = ref(null)
const avatarFile = ref(null)
const form    = ref({ nickname: auth.nickname || '' })

const initials = computed(() =>
  auth.username?.slice(0, 2).toUpperCase()
)

function handleAvatar(e) {
  const file = e.target.files[0]
  if (!file) return
  avatarFile.value = file
  preview.value = URL.createObjectURL(file)  // show preview instantly
}

async function handleSave() {
  error.value   = ''
  success.value = false
  try {
    const formData = new FormData()
    formData.append('nickname', form.value.nickname)
    if (avatarFile.value) formData.append('avatar', avatarFile.value)

    await updateProfile(formData)
    await auth.fetchProfile()  // refresh store
    success.value = true
  } catch {
    error.value = 'Ошибка при сохранении'
  }
}
</script>

<style scoped>
.profile-avatar-row { display: flex; align-items: center; gap: 16px; }
.profile-avatar { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; border: 0.5px solid var(--color-border-tertiary); }
.profile-avatar-placeholder { width: 72px; height: 72px; border-radius: 50%; background: #B5D4F4; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 500; color: #0C447C; }
.btn-upload { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 6px; border: 1px solid var(--color-border-secondary); font-size: 13px; cursor: pointer; background: var(--color-background-secondary); }
</style>
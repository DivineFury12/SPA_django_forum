<template>
  <div
    v-if="tags.length"
    class="tags-selector"
  >
    <label
      v-for="tag in tags"
      :key="tag.id"
      class="tag-option"
      :class="{ selected: modelValue.includes(tag.id) }"
    >
      <input
        type="checkbox"
        :value="tag.id"
        :checked="modelValue.includes(tag.id)"
        style="display: none;"
        @change="toggleTag(tag.id)"
      />

      {{ tag.name }}
    </label>
  </div>

  <span
    v-else
    class="empty-tags"
  >
    Нет доступных тегов
  </span>
</template>

<script setup>
const props = defineProps({
  tags: {
    type: Array,
    required: true,
  },

  modelValue: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

function toggleTag(tagId) {
  const exists = props.modelValue.includes(tagId)

  if (exists) {
    emit(
      'update:modelValue',
      props.modelValue.filter(id => id !== tagId),
    )

    return
  }

  emit(
    'update:modelValue',
    [...props.modelValue, tagId],
  )
}
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

.empty-tags {
  font-size: 13px;
  color: #888;
}
</style>
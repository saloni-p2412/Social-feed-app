<template>
  <div class="post-card">
    <div class="post-header">
      <span class="post-date">{{ formatDate(post.created_at) }}</span>
      <button
        type="button"
        class="delete-btn"
        title="Delete post"
        @click="confirmDelete"
      >
        Delete
      </button>
    </div>
    
    <div v-if="post.text_content" class="post-content">
      <p>{{ post.text_content }}</p>
    </div>

    <div v-if="post.media && post.media.length > 0" class="post-media">
      <MediaGallery :media="post.media" />
    </div>
  </div>
</template>

<script>
import MediaGallery from './MediaGallery.vue'

export default {
  name: 'PostCard',
  components: {
    MediaGallery,
  },
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  emits: ['delete'],
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    },
    confirmDelete() {
      if (window.confirm('Delete this post?')) {
        this.$emit('delete', this.post.id)
      }
    },
  },
}
</script>

<style scoped>
.post-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.post-date {
  color: #666;
  font-size: 0.9rem;
}

.delete-btn {
  padding: 0.35rem 0.65rem;
  font-size: 0.85rem;
  color: #c62828;
  background: transparent;
  border: 1px solid #ef9a9a;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn:hover {
  background: #ffebee;
  border-color: #e57373;
}

.post-content {
  margin-bottom: 1rem;
}

.post-content p {
  white-space: pre-wrap;
  word-wrap: break-word;
  line-height: 1.6;
}

.post-media {
  margin-top: 1rem;
}
</style>

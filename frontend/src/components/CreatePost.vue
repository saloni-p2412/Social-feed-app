<template>
  <div class="create-post">
    <div class="create-post-card">
      <h2>Create New Post</h2>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <textarea
            v-model="textContent"
            placeholder="What's on your mind?"
            rows="4"
            class="text-input"
          ></textarea>
        </div>

        <div class="form-group">
          <label class="file-label">
            <input
              type="file"
              ref="fileInput"
              @change="handleFileSelect"
              multiple
              accept="image/*,video/*"
              class="file-input"
            />
            <span class="file-button">Choose Images/Videos</span>
          </label>
          <div v-if="selectedFiles.length > 0" class="selected-files">
            <div v-for="(file, index) in selectedFiles" :key="index" class="file-item">
              <span>{{ file.name }}</span>
              <button type="button" @click="removeFile(index)" class="remove-btn">×</button>
            </div>
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
          <div v-if="isNetworkError" class="error-hint">
            The app is calling <strong>{{ apiBaseUrl }}/posts/</strong>. Start the backend in another terminal:
            <code>./start-backend.sh</code> or <code>cd backend && source venv/bin/activate && python manage.py runserver</code>
          </div>
        </div>

        <button type="submit" :disabled="submitting || (!textContent.trim() && selectedFiles.length === 0)" class="submit-btn">
          {{ submitting ? 'Posting...' : 'Post' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import api, { API_BASE_URL } from '../api/client'

export default {
  name: 'CreatePost',
  emits: ['post-created'],
  setup(props, { emit }) {
    const textContent = ref('')
    const selectedFiles = ref([])
    const submitting = ref(false)
    const error = ref('')
    const fileInput = ref(null)
    const apiBaseUrl = API_BASE_URL
    const isNetworkError = computed(() => {
      const e = error.value || ''
      return e.includes('Network Error') || e.includes('Failed to fetch') || e.includes('ERR_NETWORK')
    })

    const validateFiles = () => {
      const allowedImageTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
      const allowedVideoTypes = ['video/mp4', 'video/webm', 'video/ogg']
      const maxSize = 50 * 1024 * 1024 // 50MB

      for (const file of selectedFiles.value) {
        // Check file size
        if (file.size > maxSize) {
          return `File ${file.name} exceeds maximum size of 50MB`
        }

        // Check file type
        if (!allowedImageTypes.includes(file.type) && !allowedVideoTypes.includes(file.type)) {
          return `File ${file.name} has unsupported format. Allowed: images (JPEG, PNG, GIF, WebP) and videos (MP4, WebM, OGG)`
        }
      }

      return null
    }

    const handleFileSelect = (event) => {
      const files = Array.from(event.target.files)
      selectedFiles.value = [...selectedFiles.value, ...files]
      error.value = ''
    }

    const removeFile = (index) => {
      selectedFiles.value.splice(index, 1)
    }

    const handleSubmit = async () => {
      // Validate
      if (!textContent.value.trim() && selectedFiles.value.length === 0) {
        error.value = 'Post must have either text content or at least one media file'
        return
      }

      const validationError = validateFiles()
      if (validationError) {
        error.value = validationError
        return
      }

      // Submit
      submitting.value = true
      error.value = ''

      try {
        const formData = new FormData()
        formData.append('text_content', textContent.value)
        formData.append('published', 'true')

        selectedFiles.value.forEach((file) => {
          formData.append('media', file)
        })

        await api.createPost(formData)

        // Reset form
        textContent.value = ''
        selectedFiles.value = []
        if (fileInput.value) {
          fileInput.value.value = ''
        }

        // Emit event to reload posts
        emit('post-created')
      } catch (err) {
        console.error('Error creating post:', err)
        const data = err.response?.data
        if (Array.isArray(data?.errors)) {
          error.value = data.errors.join(', ')
        } else if (data?.error) {
          error.value = data.error
        } else if (data?.detail) {
          error.value = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)
        } else if (data && typeof data === 'object') {
          // e.g. serializer errors: { text_content: ['...'], published: ['...'] }
          const parts = Object.entries(data).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`)
          error.value = parts.join('; ')
        } else if (err.response?.status === 403) {
          error.value = 'Request blocked (403). If using same-site backend, check CORS and CSRF.'
        } else if (err.response?.status) {
          error.value = `Request failed (${err.response.status}). ${data ? JSON.stringify(data) : err.message}`
        } else {
          error.value = err.message || 'Failed to create post. Please try again.'
        }
      } finally {
        submitting.value = false
      }
    }

    return {
      textContent,
      selectedFiles,
      submitting,
      error,
      fileInput,
      apiBaseUrl,
      isNetworkError,
      handleFileSelect,
      removeFile,
      handleSubmit,
    }
  },
}
</script>

<style scoped>
.create-post-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.create-post-card h2 {
  margin-bottom: 1rem;
  font-size: 1.25rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.text-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  resize: vertical;
}

.text-input:focus {
  outline: none;
  border-color: #4CAF50;
}

.file-input {
  display: none;
}

.file-label {
  display: inline-block;
  cursor: pointer;
}

.file-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  color: #333;
  transition: background-color 0.2s;
}

.file-button:hover {
  background-color: #e0e0e0;
}

.selected-files {
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background-color: #f9f9f9;
  border-radius: 4px;
  font-size: 0.9rem;
}

.remove-btn {
  background: none;
  border: none;
  color: #d32f2f;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0 0.5rem;
  line-height: 1;
}

.remove-btn:hover {
  color: #b71c1c;
}

.error-message {
  color: #d32f2f;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.error-hint {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(211, 47, 47, 0.3);
  font-size: 0.85rem;
  color: #666;
}

.error-hint code {
  display: block;
  margin-top: 0.25rem;
  padding: 0.35rem 0.5rem;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #333;
}

.submit-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>

<template>
  <div class="feed-view">
  
    <CreatePost @post-created="loadPosts" />

    <!-- Show posts list when we have posts -->
    <div class="posts-container" v-if="posts.length > 0">
      <PostCard
        v-for="post in posts"
        :key="post.id"
        :post="post"
        @delete="handleDelete"
      />
    </div>

    <!-- Empty state: no posts and not loading -->
    <div v-else-if="!loading" class="empty-state">
      <p>No posts yet. Be the first to create one!</p>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading">
      <p>Loading posts...</p>
    </div>

    <!-- Show error message if something went wrong -->
    <div v-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
      <button @click="loadPosts">Try again</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../api/client'
import CreatePost from '../components/CreatePost.vue'
import PostCard from '../components/PostCard.vue'

export default {
  name: 'FeedView',
  components: {
    CreatePost,
    PostCard,
  },
  setup() {
   
    const posts = ref([])           // List of posts from API
    const loading = ref(true)      // True while fetching data
    const errorMessage = ref('')   // User-friendly error text (empty = no error)

    // --- Actions: functions that do something ---

    const loadPosts = async () => {
      errorMessage.value = ''       // Clear any previous error
      loading.value = true

      try {
        const response = await api.getPosts()
        posts.value = response.data
      } catch (error) {
        errorMessage.value = 'Failed to load posts. Please try again.'
      } finally {
        loading.value = false
      }
    }

    /**
     * Deletes a post by ID.
     */
    const handleDelete = async (postId) => {
      try {
        await api.deletePost(postId)
        loadPosts()                 // Refresh to show updated list
      } catch (error) {
       // console.error('Error deleting post:', error)
        alert('Failed to delete post. Please try again.')
      }
    }

    // --- Lifecycle: run when component appears on screen ---
    onMounted(() => {
      loadPosts()
    })

    // Expose these to the template
    return {
      posts,
      loading,
      errorMessage,
      loadPosts,
      handleDelete,
    }
  },
}
</script>

<style scoped>
.feed-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.posts-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.empty-state,
.loading {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.error-message {
  text-align: center;
  padding: 2rem;
  color: #c00;
  background: #fee;
  border-radius: 8px;
}

.error-message button {
  margin-top: 0.75rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>

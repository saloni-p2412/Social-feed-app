<template>
  <div class="feed-view">
    <CreatePost @post-created="loadPosts" />
    
    <div class="posts-container" v-if="posts.length > 0">
      <PostCard
        v-for="post in posts"
        :key="post.id"
        :post="post"
        @delete="handleDelete"
      />
    </div>
    
    <div v-else-if="!loading" class="empty-state">
      <p>No posts yet. Be the first to create one!</p>
    </div>
    
    <div v-if="loading" class="loading">
      <p>Loading posts...</p>
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
    const posts = ref([])
    const loading = ref(true)

    const loadPosts = async () => {
      try {
        loading.value = true
        const response = await api.getPosts()
        posts.value = response.data
      } catch (error) {
        console.error('Error loading posts:', error)
        alert('Failed to load posts. Please try again.')
      } finally {
        loading.value = false
      }
    }

    const handleDelete = async (postId) => {
      try {
        await api.deletePost(postId)
        loadPosts()
      } catch (error) {
        console.error('Error deleting post:', error)
        alert('Failed to delete post. Please try again.')
      }
    }

    onMounted(() => {
      loadPosts()
    })

    return {
      posts,
      loading,
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
</style>

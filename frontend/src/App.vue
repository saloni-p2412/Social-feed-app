<template>
  <div id="app">
    <header class="app-header">
      <h1>Social Feed</h1>
      <template v-if="user">
        <div class="app-nav">
          <span class="user-name">{{ user.username }}</span>
          <button type="button" class="nav-btn" @click="logout">Log out</button>
        </div>
      </template>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from './api/client'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const user = ref(null)

    const loadUser = () => {
      try {
        const stored = localStorage.getItem('user')
        user.value = stored ? JSON.parse(stored) : null
      } catch {
        user.value = null
      }
    }

    const logout = () => {
      api.clearToken()
      user.value = null
      router.push('/')
    }

    onMounted(() => {
      loadUser()
      router.afterEach(() => loadUser())
    })

    return { user, logout }
  },
}
</script>

<style>
#app {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.app-header {
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.app-nav a {
  color: #333;
  text-decoration: none;
  font-size: 0.95rem;
}

.app-nav a:hover {
  color: #4CAF50;
}

.app-nav .nav-link.router-link-active {
  color: #4CAF50;
  font-weight: 500;
}

.user-name {
  font-size: 0.95rem;
  color: #666;
}

.nav-btn {
  padding: 0.4rem 0.75rem;
  background: transparent;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
}

.nav-btn:hover {
  background: #f5f5f5;
  border-color: #ccc;
}

main {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}
</style>

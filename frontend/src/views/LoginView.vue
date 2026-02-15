<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>Log in</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <input
            v-model="username"
            type="text"
            placeholder="Username"
            class="text-input"
            
          />
        </div>
        <div class="form-group">
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            class="text-input"
           
          />
        </div>
        <div v-if="error" class="error-message">{{ error }}</div>
        <button type="submit" class="submit-btn">
          {{ 'Log in' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/client'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    // Static defaults for development (create this user with: python manage.py createsuperuser)
    const username = ref('')
    const password = ref('')
    //const submitting = ref(false)
    const error = ref('')

    // Send login request, save token, redirect to feed
    const handleSubmit = async () => {
      if (!username.value.trim() || !password.value) {
        error.value = 'Username and password are required'
        return
      }
      //submitting.value = true
      error.value = ''
      username.value = 'admin'
      password.value = 'admin123'
      try {
        const request = await api.login(username.value, password.value)
        api.setToken(request.data.token)
        if (request.data.user) {
          localStorage.setItem('user', JSON.stringify(request.data.user))
        }
        router.push('/feed')
      } catch (err) {
        // const data = err.response?.data
        error.value = 'Login failed. Please try again.'
      } 
      //finally {
        //submitting.value = false
      //}
    }

    return { username, password, error, handleSubmit }
  },
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}
.auth-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  width: 100%;
  max-width: 360px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.auth-card h2 {
  margin: 0 0 1.5rem;
  font-size: 1.5rem;
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
}
.text-input:focus {
  outline: none;
  border-color: #4CAF50;
}
.error-message {
  color: #d32f2f;
  font-size: 0.9rem;
  margin-bottom: 1rem;
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
  cursor: pointer;
}
.submit-btn:hover:not(:disabled) {
  background-color: #45a049;
}
.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>

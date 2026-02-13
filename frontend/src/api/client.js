import axios from 'axios'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const TOKEN_KEY = 'auth_token'

function getAuthHeader() {
  const token = localStorage.getItem(TOKEN_KEY)
  return token ? { Authorization: `Token ${token}` } : {}
}

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

client.interceptors.request.use((config) => {
  Object.assign(config.headers, getAuthHeader())
  return config
})

export default {
  setToken(token) {
    if (token) localStorage.setItem(TOKEN_KEY, token)
  },
  clearToken() {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem('user')
  },
  getToken() {
    return localStorage.getItem(TOKEN_KEY)
  },

  login(username, password) {
    return client.post('/auth/login/', { username, password })
  },
  register(username, password, email = '') {
    return client.post('/auth/register/', { username, password, email })
  },
  getMe() {
    return client.get('/auth/me/')
  },

  getPosts() {
    return client.get('/posts/')
  },

  createPost(formData) {
    const headers = { ...getAuthHeader() }
    return axios.post(`${API_BASE_URL}/posts/`, formData, { headers })
  },

  deletePost(id) {
    return client.delete(`/posts/${id}/`)
  },
}

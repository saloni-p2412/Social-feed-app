import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import FeedView from './views/FeedView.vue'
import LoginView from './views/LoginView.vue'
import api from './api/client'
import './style.css'

const routes = [
  { path: '/', component: LoginView },
  { path: '/feed', component: FeedView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const isLoggedIn = !!api.getToken()
  if (to.path === '/feed' && !isLoggedIn) return '/'
  if (to.path === '/' && isLoggedIn) return '/feed'
})

createApp(App).use(router).mount('#app')

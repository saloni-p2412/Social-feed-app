
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import FeedView from './views/FeedView.vue'
import LoginView from './views/LoginView.vue'
import api from './api/client'
import './style.css'

const routes = [
  { path: '/',name:"Login", component: LoginView },      // Login page
  { path: '/feed', component: FeedView },   // Main feed (posts)
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const isLoggedIn = !!api.getToken()
  if (to.path === '/feed' && !isLoggedIn) return '/'    // Protect feed
  //if (to.path === '/' && isLoggedIn) return '/feed'     // Skip login if already in
})

// Start the app
createApp(App).use(router).mount('#app')

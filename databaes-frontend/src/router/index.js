import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/Profile.vue')
  },
  {
    path: '/classes',
    name: 'classes',
    component: () => import('../views/Classes.vue')
  },
  {
    path: '/homeworkplanner',
    name: 'homeworkplanner',
    component: () => import('../views/HomeworkPlanner.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router

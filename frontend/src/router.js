import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import Categories from './views/Categories.vue'
import Brands from './views/Brands.vue'
import Products from './views/Products.vue'
import ProductImages from './views/ProductImages.vue'

const routes = [
  { path: '/login', component: Login, meta: { guest: true } },
  { path: '/', redirect: '/products' },
  { path: '/categories', component: Categories },
  { path: '/brands', component: Brands },
  { path: '/products', component: Products },
  { path: '/products/:id/images', component: ProductImages, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (!to.meta.guest && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router

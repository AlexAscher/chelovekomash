import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import Categories from './views/Categories.vue'
import Brands from './views/Brands.vue'
import Products from './views/Products.vue'
import ProductImages from './views/ProductImages.vue'
import Users from './views/Users.vue'
import Catalog from './views/Catalog.vue'
import Orders from './views/Orders.vue'

const routes = [
  { path: '/login', component: Login, meta: { guest: true } },
  { path: '/', redirect: '/catalog' },
  { path: '/catalog', component: Catalog },
  { path: '/orders', component: Orders },
  { path: '/categories', component: Categories, meta: { role: 'manager' } },
  { path: '/brands', component: Brands, meta: { role: 'manager' } },
  { path: '/products', component: Products, meta: { role: 'manager' } },
  { path: '/products/:id/images', component: ProductImages, props: true, meta: { role: 'manager' } },
  { path: '/users', component: Users, meta: { role: 'admin' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const role = localStorage.getItem('user_role') || 'user'

  if (!to.meta.guest && !token) {
    next('/login')
    return
  }

  // Проверка прав доступа по роли
  if (to.meta.role === 'admin' && role !== 'admin') {
    next('/catalog')
    return
  }
  if (to.meta.role === 'manager' && !['admin', 'manager'].includes(role)) {
    next('/catalog')
    return
  }

  next()
})

export default router

<template>
  <v-app>
    <v-navigation-drawer v-if="isLoggedIn" v-model="drawer" app>
      <v-list-item
        prepend-icon="mdi-store"
        :title="userName"
        :subtitle="roleLabel"
      />
      <v-divider />
      <v-list density="compact" nav>
        <!-- Каталог и заказы — для всех -->
        <v-list-item
          prepend-icon="mdi-storefront"
          title="Каталог"
          to="/catalog"
        />
        <v-list-item
          prepend-icon="mdi-receipt"
          title="Мои заказы"
          to="/orders"
        />

        <v-divider v-if="isAdminOrManager" class="my-2" />
        <v-list-subheader v-if="isAdminOrManager">Управление</v-list-subheader>

        <!-- Админ и менеджер — управление товарами -->
        <v-list-item
          v-if="isAdminOrManager"
          prepend-icon="mdi-shape"
          title="Категории"
          to="/categories"
        />
        <v-list-item
          v-if="isAdminOrManager"
          prepend-icon="mdi-tag"
          title="Бренды"
          to="/brands"
        />
        <v-list-item
          v-if="isAdminOrManager"
          prepend-icon="mdi-package-variant-closed"
          title="Товары"
          to="/products"
        />

        <!-- Только админ — управление пользователями -->
        <v-divider v-if="isAdmin" class="my-2" />
        <v-list-subheader v-if="isAdmin">Администрирование</v-list-subheader>
        <v-list-item
          v-if="isAdmin"
          prepend-icon="mdi-account-group"
          title="Пользователи"
          to="/users"
        />
      </v-list>
      <template #append>
        <div class="pa-2">
          <v-btn block color="red" variant="outlined" @click="logout">
            <v-icon start>mdi-logout</v-icon> Выйти
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-app-bar v-if="isLoggedIn" app color="primary">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>Интернет-магазин</v-toolbar-title>
      <v-spacer />
      <v-chip class="mr-4" variant="outlined" color="white">
        <v-icon start>mdi-account</v-icon>
        {{ userName }} ({{ roleLabel }})
      </v-chip>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <v-snackbar v-model="snack" :color="snackColor" timeout="3000">
      {{ snackText }}
    </v-snackbar>

    <!-- Уведомление менеджера о новом заказе -->
    <v-snackbar
      v-model="orderSnack"
      color="blue-darken-2"
      timeout="8000"
      location="top right"
      multi-line
    >
      <v-icon start>mdi-bell</v-icon>
      <strong>Новый заказ #{{ orderNotification.order_id }}</strong><br />
      Покупатель: {{ orderNotification.user }}<br />
      Сумма: {{ orderNotification.total }} ₽
      <template #actions>
        <v-btn variant="text" @click="orderSnack = false">Закрыть</v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref, computed, provide, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const drawer = ref(true)

const isLoggedIn = computed(() => !!localStorage.getItem('access_token'))
const userRole = computed(() => localStorage.getItem('user_role') || 'user')
const userName = computed(() => localStorage.getItem('user_name') || 'Пользователь')
const isAdmin = computed(() => userRole.value === 'admin')
const isAdminOrManager = computed(() => ['admin', 'manager'].includes(userRole.value))

const roleLabel = computed(() => {
  const map = { admin: 'Администратор', manager: 'Менеджер', user: 'Покупатель' }
  return map[userRole.value] || userRole.value
})

const snack = ref(false)
const snackText = ref('')
const snackColor = ref('success')

function showSnack(text, color = 'success') {
  snackText.value = text
  snackColor.value = color
  snack.value = true
}

provide('showSnack', showSnack)

// ── WebSocket: уведомления о заказах для менеджеров/админов ──
const orderSnack = ref(false)
const orderNotification = ref({ order_id: '', user: '', total: '' })
let ws = null

function connectWS() {
  const role = localStorage.getItem('user_role')
  if (!['admin', 'manager'].includes(role)) return
  if (ws) ws.close()
  ws = new WebSocket(`ws://${location.host}/ws/orders/`)
  ws.onmessage = (event) => {
    orderNotification.value = JSON.parse(event.data)
    orderSnack.value = true
  }
  ws.onclose = () => {
    // переподключение через 3 сек при обрыве
    setTimeout(() => {
      if (isLoggedIn.value) connectWS()
    }, 3000)
  }
}

onMounted(() => {
  if (isLoggedIn.value) connectWS()
})

watch(isLoggedIn, (val) => {
  if (val) connectWS()
  else if (ws) { ws.close(); ws = null }
})

onUnmounted(() => {
  if (ws) ws.close()
})

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')
  localStorage.removeItem('user_name')
  router.push('/login')
}
</script>

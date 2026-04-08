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
  </v-app>
</template>

<script setup>
import { ref, computed, provide } from 'vue'
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

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')
  localStorage.removeItem('user_name')
  router.push('/login')
}
</script>

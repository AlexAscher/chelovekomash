<template>
  <v-app>
    <v-navigation-drawer v-if="isLoggedIn" v-model="drawer" app>
      <v-list-item
        prepend-icon="mdi-store"
        title="Админка магазина"
        subtitle="Панель управления"
      />
      <v-divider />
      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-shape"
          title="Категории"
          to="/categories"
        />
        <v-list-item
          prepend-icon="mdi-tag"
          title="Бренды"
          to="/brands"
        />
        <v-list-item
          prepend-icon="mdi-package-variant-closed"
          title="Товары"
          to="/products"
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
  router.push('/login')
}
</script>

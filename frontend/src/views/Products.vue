<template>
  <div>
    <div class="d-flex align-center mb-4">
      <h1 class="text-h4">Товары</h1>
      <v-spacer />
      <v-btn color="primary" prepend-icon="mdi-plus" @click="openDialog()">
        Добавить
      </v-btn>
    </div>

    <v-data-table
      :headers="headers"
      :items="items"
      :loading="loading"
      class="elevation-1"
    >
      <template #item.price="{ item }">
        {{ Number(item.price).toLocaleString('ru-RU') }} ₽
      </template>
      <template #item.category="{ item }">
        {{ categoryName(item.category) }}
      </template>
      <template #item.brand="{ item }">
        {{ brandName(item.brand) }}
      </template>
      <template #item.images="{ item }">
        <v-btn size="small" variant="text" :to="`/products/${item.id}/images`">
          <v-icon start>mdi-image-multiple</v-icon>
          {{ item.images?.length || 0 }}
        </v-btn>
      </template>
      <template #item.actions="{ item }">
        <v-icon class="me-2" size="small" @click="openDialog(item)">mdi-pencil</v-icon>
        <v-icon size="small" color="red" @click="confirmDelete(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{ editingId ? 'Редактировать' : 'Создать' }} товар</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.name" label="Название" class="mb-2" />
          <v-textarea v-model="form.description" label="Описание" rows="3" class="mb-2" />
          <v-text-field v-model="form.price" label="Цена" type="number" class="mb-2" />
          <v-select
            v-model="form.category"
            :items="categories"
            item-title="name"
            item-value="id"
            label="Категория"
            class="mb-2"
          />
          <v-select
            v-model="form.brand"
            :items="brands"
            item-title="name"
            item-value="id"
            label="Бренд"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" @click="save">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог удаления -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Удалить товар?</v-card-title>
        <v-card-text>«{{ deletingItem?.name }}» будет удалён.</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="red" :loading="saving" @click="remove">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import api from '../api'

const showSnack = inject('showSnack')

const headers = [
  { title: 'ID', key: 'id', width: 60 },
  { title: 'Название', key: 'name' },
  { title: 'Цена', key: 'price', width: 140 },
  { title: 'Категория', key: 'category', width: 160 },
  { title: 'Бренд', key: 'brand', width: 140 },
  { title: 'Фото', key: 'images', sortable: false, width: 80 },
  { title: 'Действия', key: 'actions', sortable: false, width: 120 },
]

const items = ref([])
const categories = ref([])
const brands = ref([])
const loading = ref(false)
const dialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const editingId = ref(null)
const deletingItem = ref(null)
const form = ref({ name: '', description: '', price: '', category: null, brand: null })

function categoryName(id) {
  return categories.value.find(c => c.id === id)?.name || id
}

function brandName(id) {
  return brands.value.find(b => b.id === id)?.name || id
}

async function fetchAll() {
  loading.value = true
  try {
    const [prodRes, catRes, brandRes] = await Promise.all([
      api.get('/products/'),
      api.get('/categories/'),
      api.get('/brands/'),
    ])
    items.value = prodRes.data.results || prodRes.data
    categories.value = catRes.data.results || catRes.data
    brands.value = brandRes.data.results || brandRes.data
  } finally {
    loading.value = false
  }
}

function openDialog(item = null) {
  editingId.value = item ? item.id : null
  form.value = item
    ? { name: item.name, description: item.description, price: item.price, category: item.category, brand: item.brand }
    : { name: '', description: '', price: '', category: null, brand: null }
  dialog.value = true
}

function confirmDelete(item) {
  deletingItem.value = item
  deleteDialog.value = true
}

async function save() {
  saving.value = true
  try {
    const payload = { ...form.value, price: String(form.value.price) }
    if (editingId.value) {
      await api.put(`/products/${editingId.value}/`, payload)
      showSnack('Товар обновлён')
    } else {
      await api.post('/products/', payload)
      showSnack('Товар создан')
    }
    dialog.value = false
    await fetchAll()
  } catch (e) {
    const errs = e.response?.data
    const msg = errs ? Object.values(errs).flat().join(', ') : 'Ошибка'
    showSnack(msg, 'error')
  } finally {
    saving.value = false
  }
}

async function remove() {
  saving.value = true
  try {
    await api.delete(`/products/${deletingItem.value.id}/`)
    showSnack('Товар удалён')
    deleteDialog.value = false
    await fetchAll()
  } catch {
    showSnack('Ошибка удаления', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(fetchAll)
</script>

<template>
  <div>
    <div class="d-flex align-center mb-4">
      <h1 class="text-h4">Бренды</h1>
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
      <template #item.actions="{ item }">
        <v-icon class="me-2" size="small" @click="openDialog(item)">mdi-pencil</v-icon>
        <v-icon size="small" color="red" @click="confirmDelete(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{ editingId ? 'Редактировать' : 'Создать' }} бренд</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.name" label="Название" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" @click="save">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Удалить бренд?</v-card-title>
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
  { title: 'ID', key: 'id', width: 80 },
  { title: 'Название', key: 'name' },
  { title: 'Действия', key: 'actions', sortable: false, width: 120 },
]

const items = ref([])
const loading = ref(false)
const dialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const editingId = ref(null)
const deletingItem = ref(null)
const form = ref({ name: '' })

async function fetchItems() {
  loading.value = true
  try {
    const { data } = await api.get('/brands/')
    items.value = data.results || data
  } finally {
    loading.value = false
  }
}

function openDialog(item = null) {
  editingId.value = item ? item.id : null
  form.value = { name: item ? item.name : '' }
  dialog.value = true
}

function confirmDelete(item) {
  deletingItem.value = item
  deleteDialog.value = true
}

async function save() {
  saving.value = true
  try {
    if (editingId.value) {
      await api.put(`/brands/${editingId.value}/`, form.value)
      showSnack('Бренд обновлён')
    } else {
      await api.post('/brands/', form.value)
      showSnack('Бренд создан')
    }
    dialog.value = false
    await fetchItems()
  } catch (e) {
    showSnack(e.response?.data?.name?.[0] || 'Ошибка', 'error')
  } finally {
    saving.value = false
  }
}

async function remove() {
  saving.value = true
  try {
    await api.delete(`/brands/${deletingItem.value.id}/`)
    showSnack('Бренд удалён')
    deleteDialog.value = false
    await fetchItems()
  } catch {
    showSnack('Ошибка удаления', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(fetchItems)
</script>

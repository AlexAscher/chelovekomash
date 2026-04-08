<template>
  <div>
    <div class="d-flex align-center mb-4">
      <h1 class="text-h4">Пользователи</h1>
      <v-spacer />
      <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreateDialog()">
        Добавить
      </v-btn>
    </div>

    <v-data-table
      :headers="headers"
      :items="items"
      :loading="loading"
      class="elevation-1"
    >
      <template #item.role="{ item }">
        <v-chip :color="roleColor(item.role)" size="small">
          {{ roleLabel(item.role) }}
        </v-chip>
      </template>
      <template #item.actions="{ item }">
        <v-icon class="me-2" size="small" @click="openEditDialog(item)">mdi-pencil</v-icon>
        <v-icon size="small" color="red" @click="confirmDelete(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <!-- Диалог создания пользователя -->
    <v-dialog v-model="createDialog" max-width="500">
      <v-card>
        <v-card-title>Создать пользователя</v-card-title>
        <v-card-text>
          <v-text-field v-model="createForm.username" label="Логин" class="mb-2" />
          <v-text-field v-model="createForm.email" label="Email" class="mb-2" />
          <v-text-field v-model="createForm.password" label="Пароль" type="password" class="mb-2" />
          <v-select
            v-model="createForm.role"
            :items="roles"
            item-title="label"
            item-value="value"
            label="Роль"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="createDialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" @click="createUser">Создать</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог редактирования -->
    <v-dialog v-model="editDialog" max-width="500">
      <v-card>
        <v-card-title>Редактировать пользователя</v-card-title>
        <v-card-text>
          <v-text-field v-model="editForm.username" label="Логин" class="mb-2" />
          <v-text-field v-model="editForm.email" label="Email" class="mb-2" />
          <v-select
            v-model="editForm.role"
            :items="roles"
            item-title="label"
            item-value="value"
            label="Роль"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="editDialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" @click="saveEdit">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Удалить пользователя?</v-card-title>
        <v-card-text>Пользователь «{{ deletingItem?.username }}» будет удалён.</v-card-text>
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

const roles = [
  { label: 'Администратор', value: 'admin' },
  { label: 'Менеджер', value: 'manager' },
  { label: 'Пользователь', value: 'user' },
]

const headers = [
  { title: 'ID', key: 'id', width: 60 },
  { title: 'Логин', key: 'username' },
  { title: 'Email', key: 'email' },
  { title: 'Роль', key: 'role', width: 160 },
  { title: 'Действия', key: 'actions', sortable: false, width: 120 },
]

const items = ref([])
const loading = ref(false)
const saving = ref(false)

const createDialog = ref(false)
const createForm = ref({ username: '', email: '', password: '', role: 'user' })

const editDialog = ref(false)
const editForm = ref({ username: '', email: '', role: 'user' })
const editingId = ref(null)

const deleteDialog = ref(false)
const deletingItem = ref(null)

function roleColor(role) {
  if (role === 'admin') return 'red'
  if (role === 'manager') return 'orange'
  return 'green'
}

function roleLabel(role) {
  const r = roles.find(r => r.value === role)
  return r ? r.label : role
}

async function fetchItems() {
  loading.value = true
  try {
    const { data } = await api.get('/users/')
    items.value = data.results || data
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  createForm.value = { username: '', email: '', password: '', role: 'user' }
  createDialog.value = true
}

function openEditDialog(item) {
  editingId.value = item.id
  editForm.value = { username: item.username, email: item.email, role: item.role }
  editDialog.value = true
}

function confirmDelete(item) {
  deletingItem.value = item
  deleteDialog.value = true
}

async function createUser() {
  saving.value = true
  try {
    await api.post('/users/', createForm.value)
    showSnack('Пользователь создан')
    createDialog.value = false
    await fetchItems()
  } catch (e) {
    const errs = e.response?.data
    const msg = errs ? Object.values(errs).flat().join(', ') : 'Ошибка'
    showSnack(msg, 'error')
  } finally {
    saving.value = false
  }
}

async function saveEdit() {
  saving.value = true
  try {
    await api.put(`/users/${editingId.value}/`, editForm.value)
    showSnack('Пользователь обновлён')
    editDialog.value = false
    await fetchItems()
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
    await api.delete(`/users/${deletingItem.value.id}/`)
    showSnack('Пользователь удалён')
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

<template>
  <div>
    <div class="d-flex align-center mb-4">
      <v-btn icon variant="text" @click="$router.push('/products')">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <h1 class="text-h4 ml-2">Изображения товара #{{ id }}</h1>
      <v-spacer />
      <v-btn color="primary" prepend-icon="mdi-upload" @click="fileInput?.click()">
        Загрузить
      </v-btn>
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        hidden
        @change="uploadImage"
      />
    </div>

    <v-progress-linear v-if="loading" indeterminate color="primary" />

    <v-row v-if="images.length">
      <v-col v-for="img in images" :key="img.id" cols="12" sm="6" md="4" lg="3">
        <v-card>
          <v-img :src="img.image" height="200" cover />
          <v-card-actions>
            <v-spacer />
            <v-btn icon color="red" size="small" @click="confirmDelete(img)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-alert v-else type="info" variant="tonal" class="mt-4">
      У этого товара пока нет изображений.
    </v-alert>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Удалить изображение?</v-card-title>
        <v-card-text>Изображение будет удалено безвозвратно.</v-card-text>
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

const props = defineProps({ id: [String, Number] })
const showSnack = inject('showSnack')

const images = ref([])
const loading = ref(false)
const saving = ref(false)
const deleteDialog = ref(false)
const deletingItem = ref(null)
const fileInput = ref(null)

async function fetchImages() {
  loading.value = true
  try {
    const { data } = await api.get('/images/', { params: { product: props.id } })
    const all = data.results || data
    images.value = all.filter(img => String(img.product) === String(props.id))
  } finally {
    loading.value = false
  }
}

async function uploadImage(event) {
  const file = event.target.files[0]
  if (!file) return
  const formData = new FormData()
  formData.append('image', file)
  formData.append('product', props.id)
  try {
    await api.post('/images/', formData)
    showSnack('Изображение загружено')
    await fetchImages()
  } catch {
    showSnack('Ошибка загрузки', 'error')
  }
  event.target.value = ''
}

function confirmDelete(img) {
  deletingItem.value = img
  deleteDialog.value = true
}

async function remove() {
  saving.value = true
  try {
    await api.delete(`/images/${deletingItem.value.id}/`)
    showSnack('Изображение удалено')
    deleteDialog.value = false
    await fetchImages()
  } catch {
    showSnack('Ошибка удаления', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(fetchImages)
</script>

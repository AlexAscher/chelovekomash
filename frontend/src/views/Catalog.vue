<template>
  <div>
    <h1 class="text-h4 mb-4">Каталог товаров</h1>

    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

    <v-row v-if="items.length">
      <v-col v-for="product in items" :key="product.id" cols="12" sm="6" md="4" lg="3">
        <v-card class="d-flex flex-column" height="100%">
          <v-img
            :src="product.images?.length ? product.images[0].image : 'https://via.placeholder.com/300x200?text=Нет+фото'"
            height="200"
            cover
          />
          <v-card-title class="text-wrap">{{ product.name }}</v-card-title>
          <v-card-subtitle>
            {{ categoryName(product.category) }} · {{ brandName(product.brand) }}
          </v-card-subtitle>
          <v-card-text class="flex-grow-1">
            <div class="text-body-2 mb-2" style="display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">
              {{ product.description || 'Без описания' }}
            </div>
            <div class="text-h6 text-primary font-weight-bold">
              {{ Number(product.price).toLocaleString('ru-RU') }} ₽
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              variant="elevated"
              block
              prepend-icon="mdi-cart"
              :loading="buyingId === product.id"
              @click="buyProduct(product)"
            >
              Купить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-alert v-else-if="!loading" type="info" variant="tonal">
      Товаров пока нет.
    </v-alert>

    <!-- Диалог подтверждения покупки -->
    <v-dialog v-model="buyDialog" max-width="450">
      <v-card>
        <v-card-title>Оформить заказ?</v-card-title>
        <v-card-text>
          <div class="mb-2"><strong>{{ selectedProduct?.name }}</strong></div>
          <div class="mb-2">Цена: {{ selectedProduct ? Number(selectedProduct.price).toLocaleString('ru-RU') : '' }} ₽</div>
          <v-text-field
            v-model.number="quantity"
            label="Количество"
            type="number"
            min="1"
            style="max-width: 150px"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="buyDialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="ordering" @click="confirmBuy">Подтвердить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import api from '../api'

const showSnack = inject('showSnack')

const items = ref([])
const categories = ref([])
const brands = ref([])
const loading = ref(false)
const buyingId = ref(null)
const buyDialog = ref(false)
const selectedProduct = ref(null)
const quantity = ref(1)
const ordering = ref(false)

function categoryName(id) {
  return categories.value.find(c => c.id === id)?.name || ''
}

function brandName(id) {
  return brands.value.find(b => b.id === id)?.name || ''
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

function buyProduct(product) {
  selectedProduct.value = product
  quantity.value = 1
  buyDialog.value = true
}

async function confirmBuy() {
  ordering.value = true
  try {
    await api.post('/orders/', {
      items: [{ product_id: selectedProduct.value.id, quantity: quantity.value }],
    })
    showSnack('Заказ оформлен!')
    buyDialog.value = false
  } catch (e) {
    const errs = e.response?.data
    const msg = errs?.items?.[0] || errs?.detail || 'Ошибка оформления заказа'
    showSnack(msg, 'error')
  } finally {
    ordering.value = false
  }
}

onMounted(fetchAll)
</script>

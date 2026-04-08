<template>
  <div>
    <h1 class="text-h4 mb-4">Мои заказы</h1>

    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

    <v-expansion-panels v-if="orders.length" variant="accordion">
      <v-expansion-panel v-for="order in orders" :key="order.id">
        <v-expansion-panel-title>
          <div class="d-flex align-center" style="width: 100%">
            <strong class="me-4">Заказ #{{ order.id }}</strong>
            <v-chip :color="statusColor(order.status)" size="small" class="me-4">
              {{ statusLabel(order.status) }}
            </v-chip>
            <span class="text-body-2 text-medium-emphasis me-4">
              {{ new Date(order.created_at).toLocaleString('ru-RU') }}
            </span>
            <v-spacer />
            <strong>{{ Number(order.total_price).toLocaleString('ru-RU') }} ₽</strong>
          </div>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-table density="compact">
            <thead>
              <tr>
                <th>Товар</th>
                <th>Кол-во</th>
                <th>Цена</th>
                <th>Сумма</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in order.items" :key="item.id">
                <td>{{ item.product_name }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ Number(item.price).toLocaleString('ru-RU') }} ₽</td>
                <td>{{ Number(item.subtotal).toLocaleString('ru-RU') }} ₽</td>
              </tr>
            </tbody>
          </v-table>
          <div class="mt-3" v-if="order.status === 'new'">
            <v-btn
              color="red"
              variant="outlined"
              size="small"
              :loading="cancellingId === order.id"
              @click="cancelOrder(order)"
            >
              Отменить заказ
            </v-btn>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-alert v-else-if="!loading" type="info" variant="tonal">
      У вас пока нет заказов. Перейдите в <router-link to="/catalog">каталог</router-link>, чтобы оформить покупку.
    </v-alert>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import api from '../api'

const showSnack = inject('showSnack')

const orders = ref([])
const loading = ref(false)
const cancellingId = ref(null)

const statuses = {
  new: 'Новый',
  processing: 'В обработке',
  completed: 'Завершён',
  cancelled: 'Отменён',
}

function statusLabel(s) {
  return statuses[s] || s
}

function statusColor(s) {
  if (s === 'new') return 'blue'
  if (s === 'processing') return 'orange'
  if (s === 'completed') return 'green'
  if (s === 'cancelled') return 'grey'
  return 'default'
}

async function fetchOrders() {
  loading.value = true
  try {
    const { data } = await api.get('/orders/')
    orders.value = data.results || data
  } finally {
    loading.value = false
  }
}

async function cancelOrder(order) {
  cancellingId.value = order.id
  try {
    await api.post(`/orders/${order.id}/cancel/`)
    showSnack('Заказ отменён')
    await fetchOrders()
  } catch (e) {
    showSnack(e.response?.data?.detail || 'Ошибка', 'error')
  } finally {
    cancellingId.value = null
  }
}

onMounted(fetchOrders)
</script>

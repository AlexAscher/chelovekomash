from django.urls import re_path
from shop.consumers import OrderNotificationConsumer

websocket_urlpatterns = [
    re_path(r"^ws/orders/$", OrderNotificationConsumer.as_asgi()),
]

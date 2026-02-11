from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import RegisterSerializer, UserSerializer, AdminUserSerializer
from shop.permissions import IsAdmin


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя (роль = user)."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """Просмотр / редактирование своего профиля."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """Список всех пользователей (только для администратора)."""

    queryset = User.objects.all().order_by("id")
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр / изменение роли / удаление пользователя (только для администратора)."""

    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

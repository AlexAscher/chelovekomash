from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]
        read_only_fields = ["id", "role"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            role="user",
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]
        read_only_fields = ["id", "role"]


class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для администратора — может менять роль."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]
        read_only_fields = ["id"]

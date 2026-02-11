from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Администратор"),
        ("manager", "Менеджер"),
        ("user", "Пользователь"),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="user",
        verbose_name="Роль",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

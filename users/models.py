from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        # permissions = [
        #     (('can_block_users', 'Может блокировать пользователя'),)
        # ]

    def __str__(self):
        return self.email

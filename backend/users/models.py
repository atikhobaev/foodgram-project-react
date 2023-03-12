from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Имя аккаунта пользователя'
    )
    email = models.EmailField(
        max_length=250,
        unique=True,
        verbose_name='Электронная почта пользователя'
    )
    first_name = models.CharField(
        max_length=200,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name='Фамилия пользователя'
    )
    password = models.CharField(
        verbose_name='Пароль пользователя',
        max_length=100,
    )
    is_active = models.BooleanField(
        verbose_name='Активен ли пользователь',
        default=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password'
    ]

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe_user_pair'
            )
        ]

    def __str__(self):
        return f'Подписчик: {self.user} / Автор: {self.author}'

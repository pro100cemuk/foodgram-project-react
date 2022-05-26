from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор подписки'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='self_follow_prevent'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        def __str__(self):
            return f'{self.user} -> {self.author}'

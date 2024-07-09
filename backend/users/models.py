from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_username


class CustomUser(AbstractUser):
    """Своя модель юзера."""

    avatar = models.ImageField(
        'Аватар',
        upload_to='avatars',
    )
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Не более 150 символов. Только буквы, цифры и @/./+/-/_.',
        validators=[validate_username],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
    )
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True
    )
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow',
            )]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'

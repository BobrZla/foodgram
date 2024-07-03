from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_username


class User(AbstractUser):
    """Своя модель юзера."""

    username = models.CharField('Никнейм', max_length=150, unique=True, validators=[validate_username])
    email = models.EmailField('Электронная почта', max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField('Дата подписки', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow',))

    def __str__(self):
        return f'{self.user} подписан на {self.following}'

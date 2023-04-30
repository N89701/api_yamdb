from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'


class User(AbstractUser):
    email = models.EmailField(verbose_name='Электронная почта',
                              max_length=254,
                              unique=True,
                              )
    role = models.CharField('Роль',
                            max_length=50,
                            blank=True,
                            default=USER
                            )
    bio = models.TextField('Биография',
                           blank=True,
                           )
    confirmation_code = models.CharField(max_length=settings.CONFIRM_CODE_LENGTH,
                                         blank=True
                                         )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

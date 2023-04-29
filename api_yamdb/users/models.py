from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.users.validators import validate_username, validate_username_is_not_me

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'


class User(AbstractUser):
    username = models.CharField(verbose_name='Логин',
                                max_length=150,
                                null=False,
                                blank=False,
                                unique=True,
                                validators=(validate_username,
                                            validate_username_is_not_me)
                                )
    first_name = models.CharField('Имя',
                                  max_length=150,
                                  blank=True
                                  )
    last_name = models.CharField('Фамилия',
                                 max_length=150,
                                 blank=True
                                 )
    email = models.EmailField(verbose_name='Электронная почта',
                              max_length=254,
                              unique=True,
                              blank=False,
                              null=False
                              )
    role = models.CharField('Роль',
                            max_length=50,
                            blank=True,
                            default=USER
                            )
    bio = models.TextField('Биография',
                           blank=True,
                           )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

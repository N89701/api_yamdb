from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import username_validator

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

USER_ROLES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(), username_validator,),
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        blank=False,
        unique=True,
    )
    role = models.CharField(
        'Роль',
        choices=USER_ROLES,
        max_length=50,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    @property
    def is_admin(self):
        return (self.role == ADMIN or self.is_superuser or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username

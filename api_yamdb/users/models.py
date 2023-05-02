from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

USER_ROLES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    email = models.EmailField(verbose_name='Электронная почта',
                              max_length=254,
                              unique=True,
                              )
    role = models.CharField('Роль',
                            choices=USER_ROLES,
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

    @property
    def is_admin(self):
        return (self.role == 'admin' or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return self.username

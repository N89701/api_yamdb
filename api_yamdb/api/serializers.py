from rest_framework import serializers
from rest_framework.serializers import ValidationError

from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                '"me" - запрещено использовать как имя пользователя'
            )
        return value

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,
                                   max_length=254,
                                   )
    username = serializers.CharField(required=True,
                                     max_length=150,
                                     validators=[UnicodeUsernameValidator()])

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                '"me" - запрещено использовать как имя пользователя'
            )
        return value

    class Meta:
        fields = (
            'username',
            'email',
        )


class TokenObtainSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

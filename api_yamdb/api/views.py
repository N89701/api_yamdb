import random
import string

from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .serializers import SignupSerializer, TokenObtainSerializer


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = ''.join(random.choices(string.ascii_lowercase
                                                   + string.digits,
                                                   k=settings.CONFIRM_CODE_LENGTH))
        username = serializer.initial_data['username']
        email = serializer.initial_data['email']
        try:
            user, created = User.objects.get_or_create(username=username,
                                                       email=email)
        except IntegrityError:
            return Response(
                'Никнейм уже существует' if
                User.objects.filter(username='username').exists()
                else 'Email уже существует',
                status=status.HTTP_400_BAD_REQUEST)
        user.confirmation_code = confirmation_code
        user.save()
        user.email_user('Код подтверждения', confirmation_code)
        return Response(request.data, status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def obtain_token(request):
    serializer = TokenObtainSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status.HTTP_200_OK)
        return Response({'error': 'Invalid confirmation code'},
                        status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

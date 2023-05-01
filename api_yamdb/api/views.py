import random
import string

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from .serializers import SignupSerializer, TokenObtainSerializer


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = ''.join(random.choices(string.ascii_lowercase + string.digits,
                                                   k=settings.CONFIRM_CODE_LENGTH))
        new_user = serializer.save(confirmation_code=confirmation_code)
        new_user.email_user('Код подтверждения', confirmation_code)
        return Response(request.data, status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def obtain_token(request):
    serializer = TokenObtainSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        try:
            user = User.objects.get(username=username,
                                    confirmation_code=confirmation_code)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or confirmation code'},
                            status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)},
                        status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

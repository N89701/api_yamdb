import random
import string

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import SignupSerializer


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

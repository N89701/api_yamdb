from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (IsAdminOrReadOnly, IsAdminUser,
                             IsOwnerOrAdminOrModerator)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignupSerializer, TitleGetSerializer,
                             TitleCreateSerializer, TokenObtainSerializer,
                             UserSerializer, UserMeSerializer)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    field_name = []
    if user_one := User.objects.filter(username=username).first():
        field_name.append('username')
    if user_two := User.objects.filter(email=email).first():
        field_name.append('email')
    if user_one != user_two:
        return Response(field_name, status.HTTP_400_BAD_REQUEST)
    user, _created = User.objects.get_or_create(
        username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    user.email_user('Код подтверждения', confirmation_code)
    return Response(request.data, status.HTTP_200_OK)


@api_view(['POST'])
def obtain_token(request):
    serializer = TokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CategoryGenreViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                           mixins.ListModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class WithoutPutViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete',)


class TitleViewSet(WithoutPutViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'rating'
    ).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleGetSerializer
        return TitleCreateSerializer


class ReviewViewSet(WithoutPutViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrAdminOrModerator,)

    def get_title_object(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title_object().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title_object()
        )


class CommentViewSet(WithoutPutViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrAdminOrModerator,)

    def get_review_object(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review_object().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review_object()
        )


class UserViewSet(WithoutPutViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=('PATCH', 'GET',),
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=UserMeSerializer,
        detail=False,
        url_path='me',
        url_name='me'
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)

        if self.request.method == 'GET':
            return Response(serializer.data)
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

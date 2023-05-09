from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import username_validator

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=settings.MAX_LENGTH_USERNAME,
        validators=(UnicodeUsernameValidator(), username_validator,)
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    def validate(self, attrs):
        if User.objects.filter(
                username=attrs.get('username'), email=attrs.get('email')
        ).exists():
            return attrs
        if User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError(
                'Username already exists!')
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError(
                'Email already exists!')
        return super().validate(attrs)


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=settings.MAX_LENGTH_USERNAME,
        validators=(UnicodeUsernameValidator(), username_validator,)
    )
    confirmation_code = serializers.CharField(
        required=True,
    )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )

    def validate(self, attrs):
        method = self.context.get('request').method
        if method != 'POST':
            return super().validate(attrs)
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение!')
        return super().validate(attrs)

    class Meta:
        exclude = ('title',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        exclude = ('review',)
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)
        model = User


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)

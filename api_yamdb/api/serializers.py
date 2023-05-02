from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
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
    category = CategorySerializer()
    genre = GenreSerializer(many=True,)
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, attrs):
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs['title_id']
        method = self.context.get('request').method
        title = get_object_or_404(Title, pk=title_id)
        if (Review.objects.filter(author=author, title=title).exists()
                and method == 'POST'):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение!')
        return super().validate(attrs)

    class Meta:
        fields = '__all__'
        #exclude = ['title']
        read_only_fields = ('author', 'title',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )

    class Meta:
        exclude = ['review']
        read_only_fields = ('author', 'review',)
        model = Comment


class UserSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        return super().update(instance, validated_data)

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)
        model = User
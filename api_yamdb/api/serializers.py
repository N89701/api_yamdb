from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


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
    genre = GenreSerializer(many=True)
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

    def validate(self, attrs):
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs['title_id']
        method = self.context.get('request').method
        if (Review.objects.filter(author=author, title=title_id).exists()
                and method == 'POST'):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение!')
        return super().validate(attrs)

    class Meta:
        exclude = ['title']
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

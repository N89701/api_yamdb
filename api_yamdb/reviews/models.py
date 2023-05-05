from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import current_year


class Category(models.Model):
    name = models.CharField(max_length=settings.MAX_LENGTH_NAME)
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_SLUG,
        unique=True
    )

    class Meta:
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(max_length=settings.MAX_LENGTH_NAME)
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_SLUG,
        unique=True
    )

    class Meta:
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField(max_length=settings.MAX_LENGTH_NAME)
    year = models.SmallIntegerField(db_index=True, validators=[current_year])
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles'
    )

    class Meta:
        ordering = ('name', '-year')


class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.SmallIntegerField(
        validators=[MaxValueValidator(10),
                    MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review',
            ),
        )
        ordering = ('pub_date',)


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)

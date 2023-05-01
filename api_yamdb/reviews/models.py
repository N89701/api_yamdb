from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Avg

from .validators import validate_rating


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(r'^[-a-zA-Z0-9_]+$')]
    )


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(r'^[-a-zA-Z0-9_]+$')]
    )


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @property
    def rating(self):
        return self.reviews.aggregate(Avg('score'))


class Review(models.Model):
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(validators=[validate_rating])
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

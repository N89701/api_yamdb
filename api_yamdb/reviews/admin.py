from django.contrib import admin

from .models import Title, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name', 'description', 'genre', 'category')
    list_filter = ('name', 'year', 'genre', 'category')
    list_editable = ('name', 'year', 'description', 'category')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text', 'score', 'pub_date')
    search_fields = ('pk', 'author', 'title')
    list_filter = ('author', 'title', 'pub_date', 'score')
    list_editable = ('text',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'review')
    search_fields = ('text', 'review', 'author', 'pub_date')
    list_filter = ('author', 'review')
    list_editable = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    
    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
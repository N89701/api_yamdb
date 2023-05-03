# Django
from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet)
from django.urls import include, path
# Django DRF
from rest_framework.routers import DefaultRouter

from . import views
from .views import obtain_token

app_name = 'api_v1'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls), name='api-root'),
    path('v1/auth/signup/', views.signup, name='signup'),
    path('v1/auth/token/', obtain_token, name='obtain_token'),
]

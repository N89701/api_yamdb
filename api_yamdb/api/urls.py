# Django
from django.urls import include, path
# Django DRF
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api_v1'

router_v1 = DefaultRouter()
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments')
router_v1.register('users', views.UserViewSet, basename='users')

auth_patterns = [
    path('signup/', views.signup, name='signup'),
    path('token/', views.obtain_token, name='obtain_token')
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls), name='api-root')
]

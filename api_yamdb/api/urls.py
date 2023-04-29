# Django
from django.urls import include, path
# Django DRF
from rest_framework.routers import DefaultRouter

app_name = 'api_v1'

router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]

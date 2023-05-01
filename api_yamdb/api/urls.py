# Django
from django.urls import include, path
# Django DRF
from rest_framework.routers import DefaultRouter
from . import views
from .views import obtain_token

app_name = 'api_v1'

router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.signup, name='signup'),
    path('v1/auth/token/', obtain_token, name='obtain_token'),
]

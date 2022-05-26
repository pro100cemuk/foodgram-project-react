from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet)

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientsViewSet, RecipesViewSet, TagsViewSet

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('ingredients', IngredientsViewSet)
v1_router.register('tags', TagsViewSet)
v1_router.register('recipes', RecipesViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
]

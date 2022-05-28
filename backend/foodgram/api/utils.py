from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.models import Recipe
from api.serializers import RecipeToRepresentationSerializer


def post_delete_favorite_shopping_cart(request, model, obj_id):
    user = request.user
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=obj_id)
        model.objects.create(
            user=user,
            recipe=recipe
        )
        serializer = RecipeToRepresentationSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    obj = get_object_or_404(model, recipe__id=obj_id)
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

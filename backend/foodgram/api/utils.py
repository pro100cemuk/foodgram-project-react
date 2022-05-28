from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.models import Recipe
from api.serializers import FavoriteShoppingCartSerializer


def post_delete_favorite_shopping_cart(request, model, id):
    user = request.user
    if request.method == 'POST':
        data = {'user': user.id, 'recipe': id}
        serializer = FavoriteShoppingCartSerializer(
            data=data,
            context={'request': request},
            model=model
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    recipe = get_object_or_404(Recipe, id=id)
    obj = get_object_or_404(model, user=user, recipe=recipe)
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

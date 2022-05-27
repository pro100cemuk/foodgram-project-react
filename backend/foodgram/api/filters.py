from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, filters

from api.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(favorites__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(shopping_carts__user=self.request.user)


class SubscriptionFilter(FilterSet):
    recipes_limit = filters.NumberFilter(method='recipes_limit')

    def recipes_limit(self, queryset, name, value):
        return queryset.limit_recipes(value)

from django.contrib import admin

from api.models import Ingredient, IngredientRecipe, Recipe, Tag


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class TagRecipeInLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'number_of_favorites')
    inlines = (IngredientRecipeInLine, TagRecipeInLine,)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)

    def number_of_favorites(self, obj):
        return obj.favorites.count()


@admin.register(IngredientRecipe)
class AdminIngredientRecipe(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')

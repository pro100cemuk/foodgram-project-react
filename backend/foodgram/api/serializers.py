from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipesReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='ingredientrecipe_set',
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_user(self):
        return self.context.get('request').user

    def get_request(self):
        return self.context.get('request')

    def get_is_favorited(self, obj):
        request = self.get_request()
        user = self.get_user()
        if not request or request.user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.get_request()
        user = self.get_user()
        if not request or request.user.is_anonymous:
            return False
        return user.shopping_carts.filter(recipe=obj).exists()


class IngredientRecipeWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Количество ингредиента должно быть больше 0!'
            )
        return value


class RecipesWriteSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Необходимо выбрать ингредиент!'
            })
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Такой ингредиент уже выбран!'
                })
            ingredients_list.append(ingredient_id)
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Нужно выбрать тэг!'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError({
                    'tags': 'Такой тэг уже выбран!'
                })
            tags_list.append(tag)
        return data

    def create_ingredients(self, ingredients, recipe):
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient_id=ingredient['id'],
                    amount=ingredient['amount'],
                    recipe=recipe
                )
                for ingredient in ingredients
            ]
        )

    def create_tags(self, tags, recipe):
        recipe.tags.set(tags)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.ingredients.clear()
        ingredients = validated_data.get('ingredients')
        self.create_ingredients(ingredients, instance)
        instance.tags.clear()
        tags = validated_data.get('tags')
        self.create_tags(tags, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipesReadSerializer(instance, context=context).data


class RecipeToRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

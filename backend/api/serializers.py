from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import UserSerializer

from recipes.models import Ingredient, Recipe, IngredientInRecipe, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart',  'name', 'image', 'text',
                  'cooking_time', )

    @property
    def get_author(self):
        return self.context['request'].user

    @property
    def get_recipe_id(self):
        return self.context['request'].parser_context['kwargs']['pk']

    def get_is_favorited(self, recipe):
        return recipe.is_favorited(self.get_author)

    def get_is_in_shopping_cart(self, recipe):
        return recipe.is_favorited(self.get_author)

    def validate(self, data):
        if data['name'] == '':
            raise ValidationError('Название рецепта не может быть пустым')
        ingridients = data['ingredients']
        unique_ingridients = set([ingrid['id'] for ingrid in ingridients])
        if len(unique_ingridients) != len(ingridients):
            raise ValidationError(
                'Ингредиенты не могут повторяться в рецепте')
        if ingridients is None:
            raise ValidationError(
                'Количество ингредиента не может быть равно 0')
        for ingridient in ingridients:
            if ingridient['amount'] == 0:
                raise ValidationError(
                    'Количество ингредиента не может быть равно 0')
        return data

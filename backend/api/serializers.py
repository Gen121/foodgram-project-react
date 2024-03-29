from django.core.exceptions import ValidationError
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import Favorite, Follow, ShoppingCart, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_subscribed', )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Follow.is_subscribed(obj, self.context['request'].user)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id', )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True, )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True, )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeShortSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    image = Base64ImageField(required=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'text', 'cooking_time', )


class RecipeGetSerializer(RecipeShortSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True, read_only=True, )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart',  'name', 'image', 'text',
                  'cooking_time', )

    @property
    def get_user(self):
        return self.context['request'].user

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Favorite.is_in_favorite(self.get_user.pk, obj.id)

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return ShoppingCart.is_in_shopping_cart(self.get_user.pk, obj.id)


class RecipePostSerializer(RecipeGetSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(), )
    ingredients = IngredientInRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time', )

    def to_representation(self, instance):
        return RecipeGetSerializer(instance, context=self.context).data

    def validate(self, data):
        if data['name'] == '':
            raise ValidationError('Название рецепта не может быть пустым')
        ingridients = data.get('ingredients')
        unique_ingridients_id = set(
            ingrid.get('ingredient').get('id') for ingrid in ingridients)
        if len(unique_ingridients_id) != len(ingridients):
            raise ValidationError(
                'Ингредиенты не могут повторяться в рецепте')
        if ingridients is None:
            raise ValidationError(
                'Количество ингредиента не может быть меньше 0')
        for ingridient in ingridients:
            if ingridient['amount'] < 0:
                raise ValidationError(
                    'Количество ингредиента не может быть равно 0')
        if data['cooking_time'] < 0:
            raise ValidationError('Время приготовления не может быть меньше 0')
        return data

    def create_ingredients_in_recipe(self, recipe, ingredients):
        IngredientInRecipe.objects.bulk_create([IngredientInRecipe(
            recipe=recipe,
            ingredient=ingredient.get('ingredient').get('id'),
            amount=ingredient['amount'], ) for ingredient in ingredients])

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_in_recipe(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        recipe.tags.clear()
        recipe.tags.set(validated_data.pop('tags'))
        ingredient_in_recipe = IngredientInRecipe.objects.filter(recipe=recipe)
        ingredient_in_recipe.delete()
        ingredients = validated_data.pop('ingredients')
        self.create_ingredients_in_recipe(recipe, ingredients)
        return super().update(recipe, validated_data)


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count', )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
                message='Подписка на автора уже оформлена', ), ]

    @property
    def get_user(self):
        return self.context['request'].user

    def get_is_subscribed(self, obj):
        return obj.is_subscribed(self.get_user.id, obj.author.id, )

    def get_recipes(self, obj):
        recipes_limit = self.context.get(
            'request').query_params.get('recipes_limit')
        queryser = obj.author.recipes.order_by('-pub_date')
        if recipes_limit:
            queryser = queryser[:int(recipes_limit)]
        return RecipeShortSerializer(queryser, many=True).data

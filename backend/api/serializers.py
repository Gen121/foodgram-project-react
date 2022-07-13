from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from rest_framework import serializers
from shopping_cart.models import ShoppingCart
from users.models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',  'first_name', 'last_name',
            # 'is_subscribed',
            )

    # def get_is_subscribed(self, user_id):
    #     return obj.is_subscribed

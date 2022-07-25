from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.serializers import RecipeShortSerializer
from recipes.models import IngredientInRecipe, Recipe


def data_for_funcs(request, model, pk):
    recipe_pk = pk
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    if request.method == 'POST':
        serializer = RecipeShortSerializer(recipe)
        model.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        model.objects.get(
            user=request.user, recipe=recipe
            ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({'errors': 'Неправильный метод'},
                    status=status.HTTP_400_BAD_REQUEST)


def user_shopping_cart(user):
    shopping_cart = {}
    ingredients = IngredientInRecipe.objects.filter(
        recipe__in_shopping_cart_by=user).prefetch_related(
            'ingredient', 'recipe')
    if not ingredients:
        return None
    ingredients = ingredients.values(
        'ingredient__name', 'ingredient__measurement_unit').annotate(
            sum_of_amount=Sum('amount'))

    for ingred in ingredients:
        shopping_cart[ingred['ingredient__name']] = [
            ingred['sum_of_amount'], ingred['ingredient__measurement_unit']]

    return shopping_cart

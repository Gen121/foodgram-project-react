from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.serializers import RecipeShortSerializer
from recipes.models import IngredientInRecipe, Recipe


def data_for_funcs(request, obj, pk):
    recipe_pk = pk
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    if request.method == 'POST':
        serializer = RecipeShortSerializer(recipe)
        obj.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        if obj.objects.filter(
                user=request.user, recipe=recipe).exists():
            obj.objects.get(
                user=request.user, recipe=recipe
                ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'errors': 'Нет в списке'},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'errors': 'Неправильный метод'},
                    status=status.HTTP_400_BAD_REQUEST)


def user_shopping_cart(user):
    shopping_cart = {}
    ingredients = IngredientInRecipe.objects.filter(
        recipe__in_shopping_cart_by=user).prefetch_related(
            'ingredient', 'recipe').values_list(
        'ingredient__name', 'amount', 'ingredient__measurement_unit')
    if not ingredients:
        return None
    for ingredient in ingredients:
        if ingredient[0] not in shopping_cart:
            shopping_cart[ingredient[0]] = [ingredient[1], ingredient[2]]
        else:
            shopping_cart[ingredient[0]][0] += ingredient[1]
    return shopping_cart

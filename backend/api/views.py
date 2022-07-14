from djoser.serializers import TokenSerializer
from rest_framework import mixins, viewsets

from api.serializers import TagSerializer, IngredientSerializer
# from api.serializers import IngredientInRecipeSerializer
from recipes.models import Tag, Ingredient
# from recipes.models import IngredientInRecipe


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet, ):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


# class IngredientInRecipeViewSet(ListRetrieveViewSet):
#     queryset = IngredientInRecipe.objects.all()
#     serializer_class = IngredientInRecipeSerializer

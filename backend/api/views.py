from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from rest_framework import mixins, viewsets

from api.serializers import (IngredientInRecipeSerializer,
                             IngredientSerializer, RecipeSerializer,
                             TagSerializer)


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


class IngredientInRecipeViewSet(ListRetrieveViewSet):
    queryset = IngredientInRecipe.objects.all()
    serializer_class = IngredientInRecipeSerializer


class RecipeViewSet(mixins.ListModelMixin,
                    # mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    # mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,Z
                    viewsets.GenericViewSet, ):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

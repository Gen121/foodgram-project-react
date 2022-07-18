from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from rest_framework import mixins, viewsets

from users.models import User
from api.serializers import (IngredientInRecipeGetSerializer,
                             IngredientSerializer, RecipeGetSerializer,
                             RecipePostSerializer, TagSerializer)


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
    serializer_class = IngredientInRecipeGetSerializer


class RecipeViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,Z
                    viewsets.GenericViewSet, ):
    queryset = Recipe.objects.prefetch_related('ingredients').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        serializer.save(author=User.objects.all().first().profile)

    def perform_update(self, serializer):
        serializer.save(author=User.objects.all().first().profile)

    def perform_destroy(self, instance):
        instance.delete()

from django_filters.rest_framework import (CharFilter, FilterSet,
                                           AllValuesMultipleFilter)

from recipes.models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(
        field_name='tags__name',
        lookup_expr='exact', )

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='istartswith', )

    class Meta:
        model = Ingredient
        fields = ('name',)

from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class RecipeFilter(FilterSet):
    author = filters.AllValuesFilter(field_name='author')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart', )

    def get_is_favorited(self, queryset, name, data):
        if data and not self.request.user.is_anonymous:
            return queryset.filter(in_favorites_by=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, data):
        if data and not self.request.user.is_anonymous:
            return queryset.filter(
                in_shopping_cart_by=self.request.user)
        return queryset


class IngredientFilter(SearchFilter):
    search_param = 'name'

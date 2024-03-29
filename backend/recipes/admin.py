from django.contrib import admin

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import Favorite


class RecipeIngredientsInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1
    min_num = 1
    fk_name = 'recipe'
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 0
    fk_name = 'recipe'
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'in_favorite')
    fields = ('name', 'text', 'image', 'author', 'cooking_time', )
    inlines = (RecipeIngredientsInline, TagInline, )
    search_fields = ('author', 'name', 'tags__name', )
    list_filter = ('author', 'name', 'tags__name', )
    empty_value_display = '-пусто-'

    def in_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('^name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',
        'amount', )
    search_fields = ('ingredient__name',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'

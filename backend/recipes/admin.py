from django.contrib import admin

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import Profile, User

admin.site.register(Ingredient)
admin.site.register(IngredientInRecipe)
admin.site.register(Tag)


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
    fields = ('name', 'text', 'image', 'author', 'cooking_time', )
    inlines = [RecipeIngredientsInline, TagInline, ]

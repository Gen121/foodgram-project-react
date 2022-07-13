from django.contrib import admin

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag

admin.site.register(Ingredient)
admin.site.register(IngredientInRecipe)
admin.site.register(Recipe)
admin.site.register(Tag)

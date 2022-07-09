from typing import List

from django.db import models


class ShoppingCart(models.Model):
    recipes = models.ManyToManyField('recipes.Recipe', related_name='carts')
    buyer = models.OneToOneField('users.UserProfile', on_delete=models.CASCADE)
    # TODO:

    def get_shopping_list(self) -> List['recipes.Ingredient']:
        q = self.recipes.ingredients.all()
        shoping_list = dict()
        for ingredient in q:
            if ingredient.id not in shoping_list:
                shoping_list[ingredient.id] = ingredient
            else:
                shoping_list[ingredient.id].amount += ingredient.amount
        return list(shoping_list.values())

from typing import List

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from recipes.models import Ingredient, Recipe
from users.models import Profile


class ShoppingCart(models.Model):
    recipes = models.ManyToManyField(
        Recipe,
        related_name='in_shopping_carts',
        )
    buyer = models.OneToOneField(
        Profile,
        related_name='cart',
        on_delete=models.CASCADE, )

    def get_shopping_list(self) -> List['Ingredient']:
        q = self.recipes.ingredients.all()
        shoping_list = dict()
        for ingredient in q:
            if ingredient.id not in shoping_list:
                shoping_list[ingredient.id] = ingredient
            else:
                shoping_list[ingredient.id].amount += ingredient.amount
        return list(shoping_list.values())


@receiver(post_save, sender=Profile)
def create_profile_handler(sender, instance, created, **kwargs) -> None:
    if not created:
        return
    # Create the profile object, only if it is newly created
    shoping_cart = ShoppingCart(user=instance)
    shoping_cart.save()

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        related_name='profile',
        on_delete=models.CASCADE, )
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True, )
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        related_name='favorited_by',
        blank=True, )
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='in_shopping_cart',
        blank=True, )

    class Meta:
        ordering = ['user', ]
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return self.user.username + '_profile'

    def get_shopping_list(self):
        q = self.recipes.ingredients.all()
        shoping_list = dict()
        for ingredient in q:
            if ingredient.id not in shoping_list:
                shoping_list[ingredient.id] = ingredient
            else:
                shoping_list[ingredient.id].amount += ingredient.amount
        return list(shoping_list.values())

    def is_subscribed(self, user_id):
        return bool(self.following.filter(id=user_id).exists())

    def is_recipe_in_favorited(self, recipe_id):
        return bool(self.favorites.filter(id=recipe_id).exists())

    def is_recipe_in_shopping_cart(self, recipe_id):
        return bool(self.shopping_cart.filter(id=recipe_id).exists())


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_handler(sender, instance, created, **kwargs) -> None:
    if not created:
        return
    profile = Profile(user=instance)
    profile.save()

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Follow(models.Model):
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='following', )
    author = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='followers', )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'author', ], name='unique_follow', ), ]

    def __str__(self):
        return f'{self.profile} follow to {self.author}'


class Favorite(models.Model):
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        verbose_name='Пользователь', )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт', )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=['profile', 'recipe'],
                                    name='unique_favorite_recipe')
        ]

    def __str__(self):
        return f"{self.recipe} in {self.profile}'s favorites"


class ShoppingCart(models.Model):
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        verbose_name='Пользователь', )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт', )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f"{self.recipe} in {self.profile}'s shopping cart"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        related_name='profile',
        on_delete=models.CASCADE, )
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        related_name='in_favorites_by',
        through='Favorite',
        blank=True, )
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='in_shopping_cart_by',
        through='ShoppingCart',
        blank=True, )

    class Meta:
        ordering = ['user', ]
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

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

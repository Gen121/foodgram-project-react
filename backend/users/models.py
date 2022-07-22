from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False, )
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        related_name='in_favorites_by',
        through='Favorite',
        blank=True,
        verbose_name='Избранные рецепты', )
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='in_shopping_cart_by',
        through='ShoppingCart',
        blank=True,
        verbose_name='Список покупок', )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['username', ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='following', )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='followers', )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author', ], name='unique_follow', ), ]

    def __str__(self):
        return f'{self.user} follow to {self.author}'

    @classmethod
    def is_subscribed(cls, user_id, author_id):
        return bool(
            cls.objects.filter(user=user_id, author=author_id).exists())


class Favorite(models.Model):
    user = models.ForeignKey(
        'User',
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
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite_recipe')
        ]

    def __str__(self):
        return f"{self.recipe} in {self.user}'s favorites"

    @classmethod
    def is_in_favorite(cls, user_id, recipe_id):
        return bool(
            cls.objects.filter(user=user_id, recipe=recipe_id).exists())


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        'User',
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
        return f"{self.recipe} in {self.user}'s shopping cart"

    @classmethod
    def is_in_shopping_cart(cls, user_id, recipe_id):
        return bool(
            cls.objects.filter(user=user_id, recipe=recipe_id).exists())

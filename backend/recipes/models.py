from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Recipe(models.Model):
    name = models.CharField(  # in min_recipie + id
        max_length=200, )

    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        null=True, )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes', )

    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipes',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'), )

    image = models.ImageField(  # in min_recipie
        upload_to='images/',
        default='images/None/no-img.jpg', )

    text = models.TextField(
        max_length=2048, )

    cooking_time = models.IntegerField(  # in min_recipie
        validators=[MinValueValidator(1)], )

    pub_date = models.DateTimeField(
        auto_now_add=True, )

    # TODO: carts

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Recipes'
        verbose_name = 'Recipe'
        ordering = ['-pub_date']
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=('author', 'name'),
        #         name='unique_review'
        #     )]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, )
    measurement_unit = models.CharField(
        max_length=200, )


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        'recipes.Recipe',
        related_name='recipes',
        on_delete=models.CASCADE,
        )

    ingredient = models.ForeignKey(
        'recipes.Ingredient',
        related_name='Ingredients',
        on_delete=models.CASCADE  # TODO продумать сценарии удаления
    )

    amount = models.IntegerField(validators=[MinValueValidator(1)])


class Tag(models.Model):
    name = models.CharField(
        max_length=200, )

    color = models.CharField(
        null=True,
        max_length=7,
        validators=[RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$')], )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[RegexValidator(r'[-a-zA-Z0-9_]+$')], )

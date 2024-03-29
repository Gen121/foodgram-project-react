from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Recipe(models.Model):
    name = models.CharField(
        max_length=200, )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes', )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='recipes', )
    image = models.ImageField(
        upload_to='images/',
        default='images/None/no-img.jpg', )
    text = models.TextField(
        max_length=2048, )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1), ], )
    pub_date = models.DateTimeField(
        auto_now_add=True, )

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'name', ),
                name='unique_recipe_name', ), ]

    def __str__(self):
        return f'Рецепт {self.name} от {self.author}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Ингредиент', )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения', )

    class Meta:
        ordering = ['name', ]
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.name}: {self.measurement_unit}'


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        'recipes.Recipe',
        related_name='ingredients',
        on_delete=models.CASCADE,
        verbose_name='рецепт', )
    ingredient = models.ForeignKey(
        'recipes.Ingredient',
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='ингредиент', )
    amount = models.IntegerField(validators=[MinValueValidator(1), ], )

    class Meta:
        ordering = ['recipe', 'ingredient', ]
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique_ingredient'), ]

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}: {self.amount}'


class Tag(models.Model):
    name = models.CharField(
        max_length=200, )
    color = models.CharField(
        null=True,
        max_length=7,
        validators=[RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$'), ], )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[RegexValidator(r'[-a-zA-Z0-9_]+$'), ], )

    class Meta:
        ordering = ['name', ]
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return f'#{self.slug}'

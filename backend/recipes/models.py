from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Recipe(models.Model):
    name = models.CharField(  # in min_recipie + id
        max_length=200, )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes', )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes', )
    # ingredients = models.ManyToManyField(
    #     'Ingredient',
    #     related_name='recipes',
    #     through='IngredientInRecipe',
    #     through_fields=('recipe', 'ingredient', ), )
    image = models.ImageField(  # in min_recipie
        upload_to='images/',
        default='images/None/no-img.jpg', )
    text = models.TextField(
        max_length=2048, )
    cooking_time = models.IntegerField(  # in min_recipie
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

    # def is_favored(self, request):
    #     return bool(request.user.profile.favorites.filter(id=self.id).exists())  # TODO: Select_related?

    def is_favorited(self, request):
        try:
            request.user.is_authenticated
            return bool(request.user.select_related(
                'profile').is_recipe_in_favorited(self.id))
        except AttributeError:
            return False

    def is_in_shopping_cart(self, request):
        try:
            request.user.is_authenticated
            return bool(request.user.select_related(
                'profile').is_recipe_in_shopping_cart(self.id))
        except AttributeError:
            return False


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, )
    measurement_unit = models.CharField(
        max_length=200, )

    class Meta:
        ordering = ['name', ]
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.name}: {self.measurement_unit}'


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        'recipes.Recipe',
        related_name='recipes',
        on_delete=models.CASCADE, )

    ingredient = models.ForeignKey(
        'recipes.Ingredient',
        related_name='Ingredients',
        on_delete=models.CASCADE, )  # TODO продумать сценарии удаления

    amount = models.IntegerField(validators=[MinValueValidator(1), ], )

    class Meta:
        ordering = ['recipe', 'ingredient', ]
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'ингредиенты в рецептах'

        # constraints = [  #TODO: реализовать
        #     models.UniqueConstraint(
        #         fields=['recipe', 'ingredient'], name='unique_ingredient'), ]

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

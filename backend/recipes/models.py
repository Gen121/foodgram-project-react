from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

# User = get_user_model()


# class Recipe(models.Model):
#     name = models.CharField(max_length=200)

#     tags = models.ManyToManyField('Tag', related_name='recipes', null=True,)

#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='recipes', )

#     image = models.ImageField(upload_to='images/',
#                               default='images/None/no-img.jpg')
#     text = models.TextField(max_length=2048)

#     cooking_time = models.IntegerField(validators=[MinValueValidator(1)])

#     pub_date = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_at']
#         verbose_name_plural = 'Recipes'
#         verbose_name = 'Recipe'
#         ordering = ['-pub_date']
#         # constraints = [
#         #     models.UniqueConstraint(
#         #         fields=('author', 'title'),
#         #         name='unique_review'
#         #     )]

#     def __str__(self):
#         return self.name


# class Ingredient(models.Model):
#     name = models.CharField(max_length=200)
#     measurement_unit = models.CharField(max_length=200)
#     # recipes = models.ManyToManyField('Recipe',
#     #                                  related_name='ingredients',
#     #                                  null=True,)


# class Ingredient2recipe(models.Model):
#     recipe = models.ForeignKey(
#         'recipes.Recipe',
#         related_name='recipes',
#         on_delete=models.CASCADE,
#         )

#     ingredient = models.ForeignKey(
#         'recipes.Ingredient',
#         related_name='Ingredients',
#         on_delete=models.CASCADE  #TODO продумать сценарии удаления
#     )

#     amount = models.IntegerField(validators=[MinValueValidator(1)])


# class Tag(models.Model):
#     name = models.CharField(max_length=200)

#     color = models.CharField(
#         null=True,
#         max_length=7,
#         validators=[RegexValidator('[-a-zA-Z0-9_]+$')],
#         )

#     slug = models.SlugField(
#         max_length=200,
#         unique=True,
#         validators=[RegexValidator(r'[-a-zA-Z0-9_]+$')],
#         )

#     recipes = models.ManyToManyField(
#         'Recipe',
#         related_name='tags',
#         null=True,
#         )

class Parent(models.Model):
    slug = models.SlugField(max_length=255, unique=True)


class ChildOne2One(Parent):
    name = models.CharField(max_length=255)

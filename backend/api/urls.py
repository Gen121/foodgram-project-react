from django.urls import include, path
from rest_framework import routers

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register(r'tags/(?P<tag_id>[0-9]+)', TagViewSet, basename='tag_detail')

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register(r'ingredients/(?P<tag_id>[0-9]+)',
                IngredientViewSet, basename='ingredient_detail', )

router.register('recipes', RecipeViewSet, basename='recipes')
router.register(r'recipes/(?P<recipe_id>[0-9]+)',
                RecipeViewSet, basename='recipe_detail')

router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls), ),
    path('auth/', include('djoser.urls.authtoken')),
]

from django.urls import include, path
from rest_framework import routers

from api.views import TagViewSet, IngredientViewSet
# from api.views import IngredientInRecipe

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register(r'tags/(?P<tag_id>[0-9]+)', TagViewSet, basename='tag_detail')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register(r'ingredients/(?P<tag_id>[0-9]+)',
                IngredientViewSet,
                basename='ingredient_detail', )

urlpatterns = [
    path('', include(router.urls), ),
]

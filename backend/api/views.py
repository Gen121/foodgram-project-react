from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.paginations import PagePagination
from api.serializers import (CustomUserSerializer, FollowSerializer,
                             IngredientInRecipeGetSerializer,
                             IngredientSerializer, RecipeGetSerializer,
                             RecipePostSerializer, TagSerializer)
from api.utils import data_for_funcs, user_shopping_cart
from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import Follow, ShoppingCart, Favorite, User
from users.permissions import IsAuthorOrReadOnly


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet, ):
    pass


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = PagePagination

    def get_serializer_class(self):
        if self.action == 'subscribe':
            return FollowSerializer
        return CustomUserSerializer

    @action(
        detail=False, methods=['GET'], permission_classes=(IsAuthenticated,), )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, permission_classes=[IsAuthenticated], )
    def subscriptions(self, request):
        queryset = Follow.objects.filter(profile=request.user.profile)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            page,
            many=True,
            context={'request': request}, )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated], )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = FollowSerializer(
                Follow.objects.create(user=request.user, author=author),
                context={'request': request}, )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            Follow.objects.filter(
                user=request.user,
                author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('ingredients').all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = PagePagination
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user.profile)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return data_for_funcs(request, Favorite, pk)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return data_for_funcs(request, ShoppingCart, pk)

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_cart = user_shopping_cart(user=request.user)
        if not shopping_cart:
            return Response('Список покупок пуст', status=status.HTTP_200_OK, )
        shopping_list = []
        for shopping, value in shopping_cart.items():
            shopping_list.append(f'{shopping} - {value[0]}, {value[1]}\n')
        response = HttpResponse(
            shopping_list, 'Content-Type: text/plain; charset=utf-8', )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"')
        return response

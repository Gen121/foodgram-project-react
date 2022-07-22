from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Favorite, Follow, ShoppingCart, User


class FollowingInline(admin.TabularInline):
    model = Follow
    extra = 0
    fk_name = 'user'
    verbose_name = 'Аккаунт в подписки'
    verbose_name_plural = 'Подписки'


class FavoritesInline(admin.TabularInline):
    model = Favorite
    extra = 0
    fk_name = 'user'
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Избранное'


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 0
    fk_name = 'user'
    verbose_name = 'Список продуктов'
    verbose_name_plural = 'Корзина'


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserCreationForm.Meta.model
        fields = '__all__'
        field_classes = UserCreationForm.Meta.field_classes


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    list_display = ('username', 'id', 'email', 'is_staff')
    add_fieldsets = (
        (None, {'fields': (
            'username', 'password1', 'password2')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': (
            'last_login', 'date_joined')}), )
    inlines = [FollowingInline, FavoritesInline, ShoppingCartInline]
    search_fields = ('username', )
    list_filter = ('username', 'email', )
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', )
    search_fields = ('user', 'recipe', )
    list_filter = ('user', 'recipe', )
    ordering = ('user', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', )
    search_fields = ('user', 'author', )
    list_filter = ('user', 'author', )
    empty_value_display = '-пусто-'
    ordering = ('user', )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', )
    search_fields = ('user', 'recipe', )
    list_filter = ('user', 'recipe', )
    empty_value_display = '-пусто-'
    ordering = ('user', )

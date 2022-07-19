from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Favorite, Follow, Profile, ShoppingCart, User


class FollowingInline(admin.TabularInline):
    model = Follow
    extra = 0
    fk_name = 'profile'
    verbose_name = 'Аккаунт в подписки'
    verbose_name_plural = 'Подписки'


class FavoritesInline(admin.TabularInline):
    model = Favorite
    extra = 0
    fk_name = 'profile'
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Избранное'


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 0
    fk_name = 'profile'
    verbose_name = 'Список продуктов'
    verbose_name_plural = 'Корзина'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes_count', 'following_count',
                    'followers_count', 'favorites_count', )
    inlines = [FollowingInline, FavoritesInline, ShoppingCartInline]
    ordering = ('user', )

    def recipes_count(self, obj):
        return obj.recipes.count()

    def following_count(self, obj):
        return obj.following.count()

    def followers_count(self, obj):
        return obj.followers.count()

    def favorites_count(self, obj):
        return obj.favorites.count()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserCreationForm.Meta.model
        fields = '__all__'
        field_classes = UserCreationForm.Meta.field_classes


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
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
    search_fields = ('username', )
    list_filter = ('username', 'email', )
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('profile', 'recipe', )
    search_fields = ('profile', 'recipe', )
    list_filter = ('profile', 'recipe', )
    ordering = ('profile', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('profile', 'author', )
    search_fields = ('profile', 'author', )
    list_filter = ('profile', 'author', )
    empty_value_display = '-пусто-'
    ordering = ('profile', )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('profile', 'recipe', )
    search_fields = ('profile', 'recipe', )
    list_filter = ('profile', 'recipe', )
    empty_value_display = '-пусто-'
    ordering = ('profile', )

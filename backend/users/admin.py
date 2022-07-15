from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Profile, User


class FollowingInline(admin.TabularInline):
    model = Profile.following.through
    extra = 0
    fk_name = 'to_profile'
    verbose_name = 'Аккаунт в подписки'
    verbose_name_plural = 'Подписки'



class FavoritesInline(admin.TabularInline):
    model = Profile.favorites.through
    extra = 0
    fk_name = 'profile'
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Избранное'


class ShoppingCartInline(admin.TabularInline):
    model = Profile.shopping_cart.through
    extra = 0
    fk_name = 'profile'
    verbose_name = 'Продукт'
    verbose_name_plural = 'Корзина'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', )
    inlines = [FollowingInline, FavoritesInline, ShoppingCartInline]


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

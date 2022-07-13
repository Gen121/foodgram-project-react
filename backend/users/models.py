from django.conf import settings
from django.contrib.auth import get_user_model  # импортнуть модель юзера так?
# from django.contrib.auth.models import User  # <- в документации предлагают так
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.urls import reverse

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # <- Возможно следует использовать тут get_user_model(),
        primary_key=True,          # или класс User а не settings.AUTH_USER_MODEL ???
        related_name='profile',
        on_delete=models.CASCADE, )
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True, )
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        related_name='favorited_by',
        blank=True, )

    class Meta:
        ordering = ['user', ]
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return self.user.username + '_profile'

    # def get_absolute_url(self):
    #     return reverse(
    #         'users:profile_detail',
    #         kwargs={'pk': self.pk}, )

    def is_subscribed(self, user_id):
        return bool(self.user.following.filter(id=user_id).exists())


@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # <- И тут тоже
def create_profile_handler(sender, instance, created, **kwargs) -> None:
    if not created:
        return
    # Create the profile object, only if it is newly created
    profile = Profile(user=instance)
    profile.save()

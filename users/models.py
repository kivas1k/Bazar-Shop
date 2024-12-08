import os
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def clean(self):
        if self.avatar and self.avatar.size > 2 * 1024 * 1024:
            raise ValidationError("Размер аватара не должен превышать 2 МБ")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            max_size = (300, 300)
            if img.height > max_size[0] or img.width > max_size[1]:
                img.thumbnail(max_size)
                img.save(self.avatar.path)

    def delete(self, *args, **kwargs):
        if self.avatar and os.path.exists(self.avatar.path):
            os.remove(self.avatar.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Профиль пользователя: {self.user.username}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

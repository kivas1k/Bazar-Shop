from django.contrib.auth.models import User
from django.db import models
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    user_comment = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # Поле для аватара

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Сначала сохраняем, чтобы получить путь к файлу
        super().save(*args, **kwargs)

        # Изменяем размер изображения, если оно превышает 300x300
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.avatar.path)  # Сохраняем только уменьшенное изображение

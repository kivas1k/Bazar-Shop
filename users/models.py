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
        # Если аватар существует, изменим его размер
        if self.avatar:
            img = Image.open(self.avatar)
            # Если изображение больше чем 300x300, изменяем его размер
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.avatar.path)  # Сохраняем измененное изображение
        super().save(*args, **kwargs)  # Не забываем вызвать save родительского класса

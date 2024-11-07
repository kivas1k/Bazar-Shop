from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Post(models.Model):
    custom_id = models.CharField(max_length=255, unique=True)  # Кастомное уникальное ID, которое будет назначаться вручную
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)  # Картинка поста

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Если есть изображение, обработаем его с использованием Pillow
        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((800, 800))  # Изменяем размер изображения до 800x800 пикселей
            img.save(self.image.path)  # Сохраняем измененное изображение

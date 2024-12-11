import os
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from PIL import Image


class Post(models.Model):
    custom_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def clean(self):
        # Проверка на пустой custom_id
        if not self.custom_id:
            raise ValidationError('Поле custom_id не может быть пустым')
        # Проверка на превышение максимальной длины custom_id
        if len(self.custom_id) > 255:
            raise ValidationError('Поле custom_id не может быть длиннее 255 символов')

        # Проверка на пустой title
        if not self.title:
            raise ValidationError('Поле title не может быть пустым')
        # Проверка на превышение максимальной длины title
        if len(self.title) > 255:
            raise ValidationError('Поле title не может быть длиннее 255 символов')

    def save(self, *args, **kwargs):
        # Вызов метода clean для проверки валидации перед сохранением
        self.clean()
        super().save(*args, **kwargs)

        # Сжатие изображения, если оно существует
        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((800, 800))
            img.save(self.image.path)

    def delete(self, *args, **kwargs):
        # Удаление связанного изображения при удалении поста
        if self.image and os.path.exists(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

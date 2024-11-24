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

        if not self.custom_id:
            raise ValidationError('Поле custom_id не может быть пустым')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((800, 800))
            img.save(self.image.path)

    def __str__(self):
        return self.title
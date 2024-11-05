from django.db import models
from PIL import Image

class Category(models.Model):
    custom_id = models.CharField(max_length=10, unique=True)  # Кастомный ID
    name = models.CharField(max_length=255)
    pic_cat = models.ImageField(upload_to='categories/')
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Открываем изображение с помощью Pillow
        img = Image.open(self.pic_cat.path)
        # Изменяем размер изображения, если нужно
        img.thumbnail((300, 300))  # Например, до 300x300 пикселей
        img.save(self.pic_cat.path)  # Сохраняем измененное изображение

class Product(models.Model):
    custom_id = models.CharField(max_length=10, unique=True)  # Кастомный ID
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Открываем изображение с помощью Pillow
        img = Image.open(self.picture.path)
        # Изменяем размер изображения, если нужно
        img.thumbnail((300, 300))  # Например, до 300x300 пикселей
        img.save(self.picture.path)  # Сохраняем измененное изображение

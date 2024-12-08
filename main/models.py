import os
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image


def validate_positive_price(value):
    """Проверяет, что цена положительная."""
    if value <= 0:
        raise ValidationError('Цена должна быть положительной.')


class MainCategory(models.Model):
    custom_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    picture = models.ImageField(upload_to='main_categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.custom_id:
            raise ValidationError('Поле custom_id не может быть пустым')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        if self.picture:
            img = Image.open(self.picture.path)
            img.thumbnail((800, 800))
            img.save(self.picture.path)

    def delete(self, *args, **kwargs):
        if self.picture and os.path.exists(self.picture.path):
            os.remove(self.picture.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories')
    custom_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.custom_id:
            raise ValidationError('Поле custom_id не может быть пустым')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        if self.picture:
            img = Image.open(self.picture.path)
            img.thumbnail((800, 800))
            img.save(self.picture.path)

    def delete(self, *args, **kwargs):
        if self.picture and os.path.exists(self.picture.path):
            os.remove(self.picture.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    custom_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_positive_price]
    )
    picture = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.custom_id:
            raise ValidationError('Поле custom_id не может быть пустым')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        if self.picture:
            img = Image.open(self.picture.path)
            img.thumbnail((800, 800))
            img.save(self.picture.path)

    def delete(self, *args, **kwargs):
        if self.picture and os.path.exists(self.picture.path):
            os.remove(self.picture.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

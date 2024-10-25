#TODO ПЕРЕДЕЛАТЬ ЕЩЕ 1000 РАЗ
from django.db import models
from django.contrib.auth.models import User

# Модель для хранения категорий
class Category(models.Model):
    name = models.CharField(max_length=255)  # Название категории (максимум 255 символов)
    description = models.TextField(blank=True)  # Описание категории (необязательное поле)

    def __str__(self):
        return self.name  # Возвращает название категории для удобного отображения

# Модель для хранения продуктов
class Product(models.Model):
    name = models.CharField(max_length=255)  # Название продукта (максимум 255 символов)
    description = models.TextField()  # Описание продукта
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена продукта (максимум 10 цифр, 2 из которых после запятой)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)  # Связь с категорией (один продукт принадлежит одной категории)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания продукта (автоматически добавляется)

    def __str__(self):
        return self.name  # Возвращает название продукта для удобного отображения

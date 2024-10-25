#TODO ПЕРЕДЕЛАТЬ ЕЩЕ 1000 РАЗ
from django.db import models
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    pic_cat = models.ImageField(upload_to='categories/', blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    name_create = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pic_product = models.ImageField(upload_to='products/', blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)  # Добавили связь с категорией

    def __str__(self):
        return self.name

class ProductComment(models.Model):
    product = models.ForeignKey(Product, related_name='product_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.product.name}"


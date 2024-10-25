#TODO ПЕРЕДЕЛАТЬ ЕЩЕ 1000 РАЗ
from django.db import models
from users.models import User
from main.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания корзины
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления корзины

    def __str__(self):
        return f"Cart for {self.user.username}"  # Возвращает строку с информацией о корзине


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)  # Связь с корзиной
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Связь с продуктом
    quantity = models.PositiveIntegerField(default=1)  # Количество товара в корзине
    price_cat = models.DecimalField(max_digits=10, decimal_places=2)  # Цена всех товаров в корзине

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart}"  # Возвращает строку с информацией об элементе в корзине


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания заказа
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления заказа
    is_completed = models.BooleanField(default=False)  # Статус завершенности заказа

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"  # Возвращает строку с информацией о заказе


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Связь с заказом
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Связь с продуктом
    quantity = models.PositiveIntegerField(default=1)  # Количество товара в заказе
    price_orders = models.DecimalField(max_digits=10, decimal_places=2)  # Цена всех товаров в заказе

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order #{self.order.id}"  # Возвращает строку с информацией о элементе в заказе


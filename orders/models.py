from django.db import models
from django.contrib.auth.models import User
from main.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Цена за единицу товара
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Итоговая сумма за количество

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.product.price
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='order')  # Изменили на OneToOne
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order_number = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Номер заказа

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = sum(item.total_price for item in self.cart.items.all())
        if not self.order_number:
            self.order_number = f'ORD{self.pk:05d}'  # Генерация номера заказа
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

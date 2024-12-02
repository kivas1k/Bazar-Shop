from django.db import models
import uuid
from django.contrib.auth.models import User
from main.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cart_number = models.CharField(max_length=36, unique=True, blank=True, null=True)

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    def save(self, *args, **kwargs):
        if not self.cart_number:
            self.cart_number = str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = self.price or self.product.price
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"


class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создано'),
        ('waiting_confirmation', 'Ожидание подтверждения'),
        ('completed', 'Оплачено'),
        ('canceled', 'Отменено'),
        ('shipped', 'Отправлено'),
        ('delivered_signed', 'Доставлено под роспись'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cart_number = models.CharField(max_length=36, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                cart = Cart.objects.get(cart_number=self.cart_number)
                self.total_amount = cart.total_amount
            except Cart.DoesNotExist:
                pass

        if self.status == 'completed' and not self.payment_date:
            self.payment_date = self.updated_at
            self.payment_amount = self.total_amount

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"



    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Товар: {self.product.name}, Количество: {self.quantity}'


    class Meta:
        verbose_name = "Элементы заказа"
        verbose_name_plural = "Элементы заказа"


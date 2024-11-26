from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


# Админка для Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'cart_number', 'total_amount')
    search_fields = ('user__username',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    # Для отображения общей суммы корзины
    def total_amount(self, obj):
        return obj.total_amount

    total_amount.short_description = 'Общая сумма'


# Админка для CartItem
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price', 'total_price')
    search_fields = ('cart__user__username', 'product__name')
    list_filter = ('cart', 'product')

    # Для вычисления итоговой суммы
    def total_price(self, obj):
        return obj.quantity * obj.price

    total_price.short_description = 'Итоговая сумма'


# Админка для Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'cart_number', 'created_at', 'updated_at', 'total_amount', 'status', 'is_paid', 'payment_date',
    'payment_amount', 'address', 'phone_number')
    search_fields = ('user__username', 'address', 'phone_number')
    list_filter = ('created_at', 'updated_at', 'status', 'is_paid')
    ordering = ('-created_at',)


# Админка для OrderItem
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total_price')
    search_fields = ('order__user__username', 'product__name')
    list_filter = ('order', 'product')

    # Для вычисления итоговой суммы
    def total_price(self, obj):
        return obj.quantity * obj.price

    total_price.short_description = 'Итоговая сумма'

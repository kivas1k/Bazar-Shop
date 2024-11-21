from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem
from main.models import Product


# Админка для корзин
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')  # Отображаем пользователя, дату создания и обновления
    search_fields = ('user__username',)  # Поиск по имени пользователя
    list_filter = ('created_at', 'updated_at')  # Фильтрация по датам создания и обновления
    ordering = ('-created_at',)


# Админка для элементов корзины
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price',
                    'total_price')  # Отображаем корзину, товар, количество, цену и итоговую сумму
    search_fields = ('cart__user__username', 'product__name')  # Поиск по имени пользователя и имени товара
    list_filter = ('cart', 'product')  # Фильтрация по корзине и товару

    # Метод для вычисления общей стоимости
    def total_price(self, obj):
        return obj.quantity * obj.price

    total_price.short_description = 'Итоговая сумма'


# Админка для заказов
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'is_completed',
                    'total_amount')  # Отображаем пользователя, дату создания, обновления, статус и сумму
    search_fields = ('user__username',)  # Поиск по имени пользователя
    list_filter = ('is_completed', 'created_at', 'updated_at')  # Фильтрация по завершенности и датам
    ordering = ('-created_at',)

    # Поля для редактирования
    fields = ('user', 'is_completed', 'total_amount', 'created_at', 'updated_at')


# Админка для элементов заказа
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price',
                    'total_price')  # Отображаем заказ, товар, количество, цену и итоговую сумму
    search_fields = ('order__user__username', 'product__name')  # Поиск по имени пользователя и имени товара
    list_filter = ('order', 'product')  # Фильтрация по заказу и товару

    # Метод для вычисления общей стоимости
    def total_price(self, obj):
        return obj.quantity * obj.price

    total_price.short_description = 'Итоговая сумма'

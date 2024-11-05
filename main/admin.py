from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'description', 'picture')  # Отображаем все данные
    search_fields = ('name', 'category__name', 'description')
    list_filter = (
        'category',                         # Фильтр по категории
        'price',                            # Фильтр по цене
    )
    list_editable = ('price', 'category', 'description', 'picture')  # Поля, редактируемые в списке
    list_display_links = ('name',)  # Указываем, что поле 'name' будет кликабельным

    # Настраиваем поля для детальной страницы редактирования товара
    fields = ('name', 'description', 'price', 'picture', 'category')  # Указываем все поля для редактирования

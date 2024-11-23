from django.contrib import admin
from .models import Category, Product, MainCategory


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'picture')  # Отображение полей в списке
    search_fields = ('name', 'description')  # Поиск по имени и описанию
    list_filter = ('name',)  # Фильтрация по имени


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'custom_id', 'main_category', 'description', 'picture')  # Отображаем имя, ID, главную категорию, описание и картинку
    search_fields = ('name', 'custom_id', 'description')  # Поиск по имени, ID и описанию
    list_filter = ('main_category',)  # Фильтрация по главной категории


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'custom_id', 'price', 'category', 'picture')  # Отображаем имя, ID, цену, категорию и картинку
    search_fields = ('name', 'description', 'custom_id')  # Поиск по имени, описанию и ID
    list_filter = ('category', 'price')  # Фильтрация по категории и цене

    # Поля для редактирования, которые могут быть доступны только для администраторов
    readonly_fields = ('price',)


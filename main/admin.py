from django.contrib import admin
from .models import Category, Product, MainCategory


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'picture')
    search_fields = ('name', 'description')
    list_filter = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'custom_id', 'main_category', 'description', 'picture')
    search_fields = ('name', 'custom_id', 'description')
    list_filter = ('main_category',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'custom_id', 'price', 'category', 'picture')
    search_fields = ('name', 'description', 'custom_id')
    list_filter = ('category', 'price')

    readonly_fields = ('price',)


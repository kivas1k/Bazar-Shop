from django.contrib import admin
from .models import Category, Product, ProductRating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'custom_id', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'custom_id', 'price', 'category', 'rating')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    readonly_fields = ('rating',)

@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'is_like')
    list_filter = ('is_like', 'product')
    search_fields = ('product__name', 'user__username')

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),                          # Главная страница
    path('about/', views.about, name='about'),                   # Страница "О нас"
    path('catalog/', views.catalog, name='catalog'),             # Основной каталог товаров
    path('catalog/<int:cat_id>/', views.category_detail, name='category_detail'),  # Страница категории
    path('cat/<int:cat_id>/', views.product_detail, name='product_detail'),  # Страница товара по категории
    path('sales/', views.sales, name='sales'),                   # Страница акций
    path('reviews/', views.reviews, name='reviews'),             # Страница отзывов
    path('contacts/', views.contacts, name='contacts'),          # Страница контактов
]

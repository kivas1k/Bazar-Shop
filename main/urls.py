from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),                          # Главная страница
    path('about/', views.about, name='about'),                   # Страница "О нас"
    path('catalog/', views.catalog, name='catalog'),             # Основной каталог товаров
    path('catalog/<str:custom_id>/', views.category_detail, name='category_detail'),  # Страница категории
    path('cat/<str:custom_id>/', views.product_detail, name='product_detail'),  # Страница товара по категории
    path('sales/', views.sales, name='sales'),                   # Страница акций
    path('reviews/', views.reviews, name='reviews'),             # Страница отзывов
    path('contacts/', views.contacts, name='contacts'),           # Страница контактов
    path('search/', views.search_view, name='search'),           # Страница поиска
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

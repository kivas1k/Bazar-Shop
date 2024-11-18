from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('sales/', views.sales, name='sales'),
    path('reviews/', views.reviews, name='reviews'),
    path('contacts/', views.contacts, name='contacts'),
    path('search/', views.search_view, name='search'),

    path('categories/', views.all_categories, name='all_categories'),  # Общая ссылка на все категории
    path('category/<str:custom_id>/', views.category_detail, name='category_detail'),  # Отдельная категория
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<str:custom_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<str:custom_id>/', views.delete_category, name='delete_category'),

    path('catalog/', views.catalog, name='catalog'),  # Общая ссылка на все товары
    path('product/<str:custom_id>/', views.product_detail, name='product_detail'),  # Отдельный товар
    path('catalog/add/', views.add_product, name='add_product'),
    path('catalog/edit/<str:custom_id>/', views.edit_product, name='edit_product'),
    path('catalog/delete/<str:custom_id>/', views.delete_product, name='delete_product'),

    path('main_categories/', views.all_main_categories, name='all_main_categories'),  # Все главные категории
    path('main_category/<str:custom_id>/', views.main_category_detail, name='main_category_detail'),
    path('main_categories/add/', views.add_main_category, name='add_main_category'),
    path('main_categories/edit/<str:custom_id>/', views.edit_main_category, name='edit_main_category'),
    path('main_categories/delete/<str:custom_id>/', views.delete_main_category, name='delete_main_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

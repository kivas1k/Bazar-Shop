from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/all/', views.all_categories, name='all_categories'),
    path('products/all/', views.all_products, name='all_products'),
    path('catalog/<str:custom_id>/', views.category_detail, name='category_detail'),
    path('product/<str:custom_id>/', views.product_detail, name='product_detail'),
    path('sales/', views.sales, name='sales'),
    path('reviews/', views.reviews, name='reviews'),
    path('contacts/', views.contacts, name='contacts'),
    path('search/', views.search_view, name='search'),

    # Административные действия
    path('category/add/', views.add_category, name='add_category'),
    path('category/edit/<str:custom_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<str:custom_id>/', views.delete_category, name='delete_category'),

    path('product/add/', views.add_product, name='add_product'),
    path('product/edit/<str:custom_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<str:custom_id>/', views.delete_product, name='delete_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

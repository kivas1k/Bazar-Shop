from django.urls import path, register_converter
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Главная страница
    path('about/', views.about, name='about'),  # о нас
    path('cat/<int:cat_id>', views.categories, name='cat_id'),  # Каталог
    path('cat/<slug:cat_slug>', views.categories_by_slug, name='cat'),  # Каталог
]
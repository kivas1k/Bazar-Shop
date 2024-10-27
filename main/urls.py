from django.urls import path
from users.views import profile_view
from . import views
from users.views import register, login_view

urlpatterns = [
    path('', views.index, name='home'),  # Главная страница
    path('about/', views.about, name='about'),  # О нас
    path('cat/<int:cat_id>/', views.categories, name='cat_id'),  # Каталог
    path('cat/<slug:cat_slug>/', views.categories_by_slug, name='cat'),  # Каталог по slug
    path('register/', register, name='register'),  # Регистрация
    path('login/', login_view, name='login'),  # Вход
    path('search/', views.search_view, name='search'),  # Добавляем URL для поиска
    path('profile/', profile_view, name='profile'),  # Профиль пользователя
]

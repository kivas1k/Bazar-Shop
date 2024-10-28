from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),  # Добавляем маршрут для редактирования профиля
    path('logout/', views.logout_view, name='logout'),  # URL для выхода
]

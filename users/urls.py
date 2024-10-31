from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),         # Регистрация
    path('login/', views.login_view, name='login'),
    #TODO
    path('logout/', views.logout_view, name='logout'),          # Выйти из профиля

    path('profile/', views.profile_view, name='profile'),       # Профиль пользователя
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # Редактирование профиля
]

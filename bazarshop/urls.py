from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls')),         # Главная, каталог и тд
    path('users/', include('users.urls')),   # Вход, регистрация, профиль, выйти
    path('orders/', include('orders.urls')), # Корзина, заказ, оплата
    path('blog/', include('blog.urls')),     # Блог: статьи, просмотр, публикация, редактирование
]
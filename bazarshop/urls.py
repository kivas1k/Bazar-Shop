from django.contrib import admin
from django.urls import path, include
from main import views
from main.views import page_not_found


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls')),         # Главная, каталог, товар, акции, о нас, отзывы, контакты
    path('users/', include('users.urls')),   # Вход, регистрация, профиль, выйти
    path('orders/', include('orders.urls')), # Корзина, заказ, оплата
    path('blog/', include('blog.urls')),     # Блог: статьи, просмотр, публикация, редактирование
]
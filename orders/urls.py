from django.urls import path
from . import views

urlpatterns = [
#TODO все это
    path('cart/', views.cart_view, name='cart'),            # Корзина
    path('checkout/', views.checkout, name='checkout'),     # Оформление заказа
    path('payment/', views.payment, name='payment'),        # Страница оплаты
]

from django.shortcuts import render

menu = ["О нас", "Каталог", "Войти"]  # Опционально, если используется в шаблонах

def cart_view(request):
    return render(request, 'orders/cart.html', {'title': 'Корзина', 'menu': menu})

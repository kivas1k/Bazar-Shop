from django.shortcuts import render

menu = ["О нас", "Каталог", "Блог", "Акции", "Отзывы", "Контакты", "Войти"]

def cart_view(request):
    return render(request, 'orders/cart.html', {'title': 'Корзина', 'menu': menu})

def checkout(request):
    return render(request, 'orders/checkout.html', {'title': 'Оформление заказа', 'menu': menu})

def payment(request):
    return render(request, 'orders/payment.html', {'title': 'Оплата', 'menu': menu})

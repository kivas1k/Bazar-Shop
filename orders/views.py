from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
from main.models import Product
from .forms import UpdateCartItemForm, OrderForm

# Просмотр корзины
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum(item.total_price for item in items)

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
    })

# Добавление товара в корзину
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1, 'price': product.price, 'total_price': product.price})

    if not created:
        item.quantity += 1
        item.total_price = item.quantity * item.price
        item.save()

    return redirect('view_cart')

# Удаление товара из корзины
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('view_cart')

# Очистка корзины
@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()  # Удаление всех товаров из корзины
    return redirect('view_cart')

# Изменение количества товара в корзине
@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        form = UpdateCartItemForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            if new_quantity <= 0:
                item.delete()  # Если количество товара <= 0, то удаляем товар из корзины
            else:
                item.quantity = new_quantity
                item.total_price = item.price * new_quantity
                item.save()
        else:
            # Обработка ошибок формы, если они есть
            pass
    return redirect('view_cart')

# Создание заказа
@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return redirect('view_cart')

    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        order.total_amount = sum(item.total_price for item in cart.items.all())
        order.save()
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )
        cart.items.all().delete()

        return redirect('order_detail', order_id=order.id)

    return render(request, 'cart/create_order.html', {'form': form, 'cart': cart})

# Просмотр заказов
@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'cart/orders.html', {'orders': orders})

# Детализация заказа
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    return render(request, 'cart/order_detail.html', {
        'order': order,
        'items': items,
    })

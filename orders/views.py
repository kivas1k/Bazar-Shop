from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
from main.models import Product
from django.contrib import messages
from .forms import UpdateCartItemForm, OrderForm

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = cart.total_amount

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
    })

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, custom_id=product_id)  # Убедитесь, что используете custom_id
        cart, created = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )

        if not created:
            item.quantity += 1
            item.save()

        messages.success(request, f'Товар "{product.name}" добавлен в корзину.')

        return redirect('product_detail', custom_id=product.custom_id)

    return redirect('catalog')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('view_cart')

@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return redirect('view_cart')

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease' and item.quantity > 1:
            item.quantity -= 1

        item.save()

        messages.success(request, 'Количество товара обновлено.')

    return redirect('view_cart')

@login_required
def create_order(request):
    cart = Cart.objects.get(user=request.user)
    order_form = OrderForm(request.POST or None)

    if request.method == 'POST' and order_form.is_valid():
        order = order_form.save(commit=False)
        order.cart = cart
        order.user = request.user
        order.save()

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        cart.items.all().delete()  # Очистить корзину после оформления заказа
        messages.success(request, f'Ваш заказ #{order.order_number} был успешно создан!')
        return redirect('view_orders')

    return render(request, 'cart/create_order.html', {'form': order_form})

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'cart/view_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_detail.html', {'order': order})

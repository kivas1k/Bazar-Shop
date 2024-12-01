from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from main.models import Product
from .forms import UpdateCartItemForm, CheckoutForm
import uuid
from django.utils import timezone

#Нужно доделать оплату. Нужно сделать так чтобы после того как как пользователь оплатил заказ писалось что ваш заказ проходит проверку, после того как админ подтвердил заказ у пользователя отобразится что его заказ был отправлен и в течении недели будет доставлен. После того как товар будет доставлен чтобы пользователь мог как это это подтвердить, что товар доставлен. Нужно добавить какуе нибудь кнопку для подтвержения. Вот файлы views

def is_admin(user):
    return user.is_staff


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
    product = get_object_or_404(Product, id=product_id)
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
    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Товар удален из корзины.')
    return redirect('view_cart')


@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, 'Корзина очищена.')
    return redirect('view_cart')


@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        form = UpdateCartItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Количество товара обновлено.')
        else:
            messages.error(request, 'Ошибка при обновлении количества товара.')

    return redirect('view_cart')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()

    if not items:
        messages.error(request, 'Корзина пуста. Добавьте товары перед оформлением заказа.')
        return redirect('view_cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                cart_number=cart.cart_number,
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number']
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price,
                    total_price=item.total_price
                )
            cart.items.all().delete()

            cart.cart_number = str(uuid.uuid4())
            cart.save()

            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('view_cart')
        else:
            messages.error(request, 'Ошибка при оформлении заказа.')
    else:
        form = CheckoutForm()

    return render(request, 'cart/checkout.html', {
        'form': form,
        'items': items,
        'total_price': cart.total_amount
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'cart/order_history.html', {
        'orders': orders,
    })


@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        if not order.is_paid:
            order.status = 'waiting_confirmation'
            order.payment_date = timezone.now()
            order.payment_amount = order.total_amount
            order.save()

            messages.success(request, 'Оплата отправлена на проверку. Ожидайте подтверждения администратора.')
        else:
            messages.info(request, 'Оплата уже подтверждена.')

        return redirect('home')

    return render(request, 'cart/pay_order.html', {'order': order})




@login_required
def order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_status.html', {'order': order})


@login_required
@user_passes_test(is_admin)
def admin_order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'cart/admin_order_list.html', {'orders': orders})


@login_required
@user_passes_test(is_admin)
def admin_edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        allowed_statuses = ['waiting_confirmation', 'completed', 'canceled']

        if new_status in allowed_statuses:
            order.status = new_status
            if new_status == 'completed':
                order.payment_date = timezone.now()
                order.payment_amount = order.total_amount
            order.save()

            messages.success(request, f'Статус заказа #{order.id} изменен на "{order.get_status_display()}".')
        else:
            messages.error(request, 'Недопустимый статус.')

        return redirect('admin_order_list')

    return render(request, 'cart/admin_edit_order.html', {
        'order': order,
        'status_choices': Order._meta.get_field('status').choices,
    })

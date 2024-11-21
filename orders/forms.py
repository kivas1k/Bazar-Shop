from django import forms
from .models import CartItem, Order

class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']  # Только поле для изменения количества товара

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Количество товара должно быть больше нуля.')
        return quantity


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_amount', 'is_completed']  # 'total_amount' будет автоматически рассчитываться

    def clean_total_amount(self):
        total_amount = self.cleaned_data.get('total_amount')
        # Лучше не позволять пользователю вводить сумму вручную
        # Сумма должна рассчитываться на основе товаров в заказе
        if total_amount <= 0:
            raise forms.ValidationError('Сумма заказа должна быть больше нуля.')
        return total_amount

    def save(self, commit=True):
        # Вычисляем total_amount в момент сохранения
        if not self.instance.id:  # Проверяем, что заказ еще не сохранен
            cart = self.instance.cart  # Получаем корзину пользователя
            self.instance.total_amount = sum(item.total_price for item in cart.items.all())
        return super().save(commit=commit)

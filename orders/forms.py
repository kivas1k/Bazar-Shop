from django import forms
from .models import CartItem, Order

class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']  # Только поле для изменения количества

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Количество товара должно быть больше нуля.')
        return quantity


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Убираем 'created_at', чтобы избежать ошибки
        fields = ['total_amount', 'is_completed']  # Добавляем только редактируемые поля

    def clean_total_amount(self):
        total_amount = self.cleaned_data.get('total_amount')
        if total_amount <= 0:
            raise forms.ValidationError('Сумма заказа должна быть больше нуля.')
        return total_amount

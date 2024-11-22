from django import forms
from .models import CartItem, Order


class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Количество товара должно быть больше нуля.')
        return quantity


class OrderForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True, label='Имя')
    address = forms.CharField(max_length=255, required=True, label='Адрес доставки')
    phone = forms.CharField(max_length=20, required=True, label='Телефон')

    class Meta:
        model = Order
        fields = ['name', 'address', 'phone']

    def save(self, commit=True):
        if not self.instance.cart:
            raise forms.ValidationError("Заказ не может быть создан без корзины.")

        if not self.instance.total_amount:
            self.instance.total_amount = sum(item.total_price for item in self.instance.cart.items.all())

        self.instance.is_completed = False

        return super().save(commit=commit)

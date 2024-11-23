from django import forms
from .models import CartItem


class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CheckoutForm(forms.Form):
    address = forms.CharField(label='Адрес', widget=forms.Textarea(attrs={'rows': 3}))
    phone_number = forms.CharField(label='Номер телефона', max_length=15)

from django import forms
from .models import Category, Product, MainCategory


class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ['custom_id', 'name', 'description', 'picture']

    def clean_custom_id(self):
        custom_id = self.cleaned_data.get('custom_id')
        if self.instance.pk and MainCategory.objects.filter(custom_id=custom_id).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Это кастомное ID уже существует для другой главной категории!")
        return custom_id


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def clean_custom_id(self):
        custom_id = self.cleaned_data.get('custom_id')
        if self.instance.pk and Category.objects.filter(custom_id=custom_id).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Это кастомное ID уже существует для другой категории!")
        return custom_id


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_custom_id(self):
        custom_id = self.cleaned_data.get('custom_id')
        if self.instance.pk and Product.objects.filter(custom_id=custom_id).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Это кастомное ID уже существует для другого товара!")
        return custom_id

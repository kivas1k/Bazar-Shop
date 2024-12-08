from django import forms
from .models import Post
from PIL import Image as PILImage
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['custom_id', 'title', 'content', 'image']

    def clean_custom_id(self):
        custom_id = self.cleaned_data['custom_id']
        if not custom_id:
            raise forms.ValidationError('Поле custom_id не может быть пустым')
        return custom_id

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            try:
                img = PILImage.open(image)
                img.verify()  # Проверка формата изображения
            except (IOError, SyntaxError) as e:
                raise ValidationError("Неверный формат изображения. Пожалуйста, загрузите изображение в поддерживаемом формате.")
        return image

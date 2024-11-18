from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['custom_id', 'title', 'content', 'image']

    def clean_custom_id(self):
        custom_id = self.cleaned_data['custom_id']
        if not custom_id:
            raise forms.ValidationError('Поле custom_id не может быть пустым')
        return custom_id
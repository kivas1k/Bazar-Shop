from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={
        'placeholder': 'Введите ваш email',
        'class': 'form-control'
    }))

    def clean_email(self):
        """Проверка на уникальность email."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Введите имя пользователя',
                'class': 'form-control'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Введите пароль',
                'class': 'form-control'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Повторите пароль',
                'class': 'form-control'
            }),
        }

    def save(self, commit=True):
        """Сохранение пользователя с email."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Расскажите о себе',
            'class': 'form-control',
            'rows': 4
        })
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Email или Имя пользователя",
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите email или имя пользователя',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        """Инициализация формы с кастомным полем username."""
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = ''

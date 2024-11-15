from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    avatar = forms.ImageField(required=False, label="Аватар", widget=forms.ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            if self.cleaned_data.get('avatar'):
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                user_profile.avatar = self.cleaned_data['avatar']
                user_profile.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Заменяем поле на email

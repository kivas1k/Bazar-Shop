from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    avatar = forms.ImageField(required=False, label="Аватар",
                              widget=forms.ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'avatar']  # Добавили аватар в форму

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)  # Сохраняем пользователя через родительский метод

        # Если добавлен аватар, создаем или обновляем профиль пользователя
        if self.cleaned_data.get('avatar'):
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.avatar = self.cleaned_data['avatar']
            user_profile.save()

        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'user_comment', 'avatar']  # Включаем аватар, биографию и комментарий

    def save(self, *args, **kwargs):
        user_profile = super().save(*args, **kwargs)

        # Если аватар изменен, обновляем его
        if self.cleaned_data.get('avatar'):
            user_profile.avatar = self.cleaned_data['avatar']
            user_profile.save()

        return user_profile

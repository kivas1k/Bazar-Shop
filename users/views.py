from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserProfileForm, UserRegistrationForm, EmailAuthenticationForm
from .models import UserProfile

# Функция для регистрации пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизуем пользователя сразу после регистрации
            return redirect('home')  # Перенаправление на главную страницу или другую страницу
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# Функция для аутентификации пользователя (вход)
def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = EmailAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Функция для выхода пользователя
def logout_view(request):
    logout(request)
    return redirect('login')

# Просмотр профиля пользователя
@login_required
def profile(request):
    return render(request, 'users/profile.html')

# Редактирование профиля пользователя
@login_required  # Только для авторизованных пользователей
def profile_edit(request):
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_profile_form.is_valid():
            user_profile_form.save()  # Сохраняем изменения в профиле
            return redirect('profile')  # Перенаправляем на страницу профиля после сохранения
    else:
        user_profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'users/profile_edit.html', {'form': user_profile_form})

# Функция для обновления аватара пользователя
@login_required
def update_avatar(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправляем на страницу профиля
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'users/profile_edit.html', {'form': form})

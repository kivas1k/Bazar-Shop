from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserProfileForm, UserRegistrationForm, EmailAuthenticationForm
from django.conf import settings


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    user_profile = request.user.profile
    return render(request, 'users/profile.html', {'user_profile': user_profile})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('profile')
    else:
        user_profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'users/profile_edit.html', {'form': user_profile_form})

# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required

menu = ["О нас", "Каталог", "Блог", "Акции", "Отзывы", "Контакты", "Войти"]

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'menu': menu})

@login_required
def profile_view(request):
    user_profile = request.user.profile
    return render(request, 'users/profile.html', {
        'title': 'Профиль',
        'menu': menu,
        'user_profile': user_profile,
    })

@login_required
def profile_edit(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/profile_edit.html', {
        'title': 'Редактирование профиля',
        'menu': menu,
        'form': form,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Неверное имя пользователя или пароль.', 'menu': menu})
    return render(request, 'users/login.html', {'menu': menu})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def update_avatar(request):
    user_profile = request.user.profile
    if request.method == 'POST' and request.FILES.get('avatar'):
        user_profile.avatar = request.FILES['avatar']
        user_profile.save()
        return redirect('profile')
    return render(request, 'users/update_avatar.html', {'user_profile': user_profile})

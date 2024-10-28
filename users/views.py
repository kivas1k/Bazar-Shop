from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm

menu = ["О нас", "Каталог", "Войти"]  # Общая переменная для меню

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход после регистрации
            return redirect('home')  # перенаправляем на главную страницу
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'menu': menu})

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/profile.html', {'title': 'Профиль', 'menu': menu})

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


def profile_edit_view(request):

    return render(request, 'users/profile_edit.html', {'title': 'Редактирование профиля'})
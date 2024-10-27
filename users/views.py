from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически выполняем вход после регистрации
            return redirect('home')  # перенаправляем на главную страницу
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def profile_view(request):
       return render(request, 'main/profile.html', {'title': 'Профиль', 'menu': menu})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Неверное имя пользователя или пароль.'})
    return render(request, 'users/login.html')

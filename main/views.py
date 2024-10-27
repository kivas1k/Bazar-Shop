from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

menu = ["О нас", "Каталог", "Войти"]

def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
    }
    return render(request, 'main/index.html', context=data)

def about(request):
    return render(request, 'main/about.html', {'title': 'О сайте', 'menu': menu})

def categories(request, cat_id):
    return HttpResponse(f"<h1>Тут будет каталог</h1><p>id: {cat_id}</p>")

def categories_by_slug(request, cat_slug):
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")

def search_view(request):
    query = request.GET.get('query', '')

    return render(request, 'main/search_results.html', {'query': query, 'menu': menu})

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Нету тут ниче</h1>")

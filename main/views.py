from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .models import Category, Product

menu = ["О нас", "Каталог", "Блог", "Акции", "Отзывы", "Контакты", "Войти"]

def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
    }
    return render(request, 'main/index.html', context=data)

def about(request):
    return render(request, 'main/about.html', {'title': 'О сайте', 'menu': menu})

def catalog(request):
    # Список всех категорий для каталога
    categories = Category.objects.all()
    return render(request, 'main/catalog.html', {'title': 'Каталог товаров', 'menu': menu, 'categories': categories})

def category_detail(request, cat_id):
    # Страница категории товаров, где `cat_id` указывает на ID категории
    category = get_object_or_404(Category, id=cat_id)
    products = category.products.all()  # Получение всех товаров в этой категории
    return render(request, 'main/category_detail.html', {
        'title': f"Категория: {category.name}",
        'menu': menu,
        'category': category,
        'products': products
    })

def product_detail(request, cat_id):
    # Страница товара, где `cat_id` указывает на ID товара
    product = get_object_or_404(Product, id=cat_id)
    return render(request, 'main/product_detail.html', {
        'title': f"Товар: {product.name}",
        'menu': menu,
        'product': product
    })

def sales(request):
    return render(request, 'main/sales.html', {'title': 'Акции', 'menu': menu})

def reviews(request):
    return render(request, 'main/reviews.html', {'title': 'Отзывы', 'menu': menu})

def contacts(request):
    return render(request, 'main/contacts.html', {'title': 'Контакты', 'menu': menu})

def search_view(request):
    query = request.GET.get('query', '')
    results = Product.objects.filter(name__icontains=query)  # Простой поиск по названию товара
    return render(request, 'main/search_results.html', {
        'query': query,
        'title': 'Результаты поиска',
        'menu': menu,
        'results': results
    })

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

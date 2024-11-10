from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import Category, Product
from .forms import CategoryForm, ProductForm

# Меню, которое будет отображаться на каждой странице
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
    categories = Category.objects.all()
    return render(request, 'main/catalog.html', {
        'title': 'Каталог товаров',
        'menu': menu,
        'categories': categories
    })

def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'main/all_categories.html', {
        'title': 'Все категории',
        'menu': menu,
        'categories': categories
    })

def all_products(request):
    products = Product.objects.all()
    return render(request, 'main/all_products.html', {
        'title': 'Все товары',
        'menu': menu,
        'products': products
    })

def category_detail(request, custom_id):
    category = get_object_or_404(Category, custom_id=custom_id)
    products = category.products.all()
    return render(request, 'main/category_detail.html', {
        'category': category,
        'products': products,
        'title': category.name,
        'menu': menu
    })

def product_detail(request, custom_id):
    product = get_object_or_404(Product, custom_id=custom_id)
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
    results = Product.objects.filter(name__icontains=query)
    return render(request, 'main/search_results.html', {
        'query': query,
        'title': 'Результаты поиска',
        'menu': menu,
        'results': results
    })

# Функции для работы с категориями

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = CategoryForm()

    return render(request, 'main/add_category.html', {
        'form': form,
        'title': 'Добавить категорию',
        'menu': menu,
    })

def edit_category(request, custom_id):
    category = get_object_or_404(Category, custom_id=custom_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'main/edit_category.html', {
        'form': form,
        'title': 'Редактировать категорию',
        'menu': menu,
    })

def delete_category(request, custom_id):
    category = get_object_or_404(Category, custom_id=custom_id)
    category.delete()
    return redirect('catalog')

# Функции для работы с продуктами

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Добавляем поддержку файлов (картинок)
        if form.is_valid():
            form.save()
            return redirect('all_products')
    else:
        form = ProductForm()

    return render(request, 'main/add_product.html', {
        'form': form,
        'title': 'Добавить товар',
        'menu': menu,
    })

def edit_product(request, custom_id):
    product = get_object_or_404(Product, custom_id=custom_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('all_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'main/edit_product.html', {
        'form': form,
        'title': 'Редактировать товар',
        'menu': menu,
    })

def delete_product(request, custom_id):
    product = get_object_or_404(Product, custom_id=custom_id)
    product.delete()
    return redirect('all_products')

# Страница с ошибкой 404
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

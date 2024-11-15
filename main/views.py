from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Category, Product
from .forms import CategoryForm, ProductForm

menu = ["О нас", "Каталог", "Блог", "Акции", "Отзывы", "Контакты", "Войти"]

def is_admin(user):
    return user.is_superuser

def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
    }
    return render(request, 'main/index.html', context=data)

def about(request):
    return render(request, 'main/about.html', {'title': 'О сайте', 'menu': menu})

def catalog(request):
    products = Product.objects.all()  # Получаем все товары
    return render(request, 'main/catalog.html', {
        'title': 'Каталог товаров',
        'menu': menu,
        'products': products,  # Передаем только товары
    })

def product_detail(request, custom_id):
    product = get_object_or_404(Product, custom_id=custom_id)
    return render(request, 'main/product_detail.html', {
        'title': f"Товар: {product.name}",
        'menu': menu,
        'product': product
    })

def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'main/all_categories.html', {
        'title': 'Все категории',
        'menu': menu,
        'categories': categories
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

@login_required
@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_categories')  # Перенаправляем на страницу с категориями
    else:
        form = CategoryForm()
    return render(request, 'main/add_category.html', {'title': 'Добавить категорию', 'menu': menu, 'form': form})

@login_required
@user_passes_test(is_admin)
def edit_category(request, custom_id):
    category = get_object_or_404(Category, custom_id=custom_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_detail', custom_id=category.custom_id)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'main/edit_category.html', {'title': 'Редактировать категорию', 'menu': menu, 'form': form})


@login_required
@user_passes_test(is_admin)
def delete_category(request, custom_id):
    category = get_object_or_404(Category, custom_id=custom_id)
    if request.method == 'POST':
        category.delete()
        return redirect('all_categories')
    return render(request, 'main/delete_category.html', {'title': 'Удалить категорию', 'menu': menu, 'category': category})

@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'main/add_product.html', {'title': 'Добавить товар', 'menu': menu, 'form': form})

@login_required
@user_passes_test(is_admin)
def edit_product(request, custom_id):
    product = get_object_or_404(Product, custom_id=custom_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', custom_id=product.custom_id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/edit_product.html', {'title': 'Редактировать товар', 'menu': menu, 'form': form})

@login_required
@user_passes_test(is_admin)
def delete_product(request, custom_id):
    product = get_object_or_404(Product, custom_id=custom_id)
    if request.method == 'POST':
        product.delete()
        return redirect('all_products')
    return render(request, 'main/delete_product.html', {'title': 'Удалить товар', 'menu': menu, 'product': product})

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

# Страница с ошибкой 404
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

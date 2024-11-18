from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import MainCategory, Category, Product
from .forms import MainCategoryForm, CategoryForm, ProductForm

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
    products = Product.objects.all()
    return render(request, 'main/catalog.html', {
        'title': 'Каталог товаров',
        'menu': menu,
        'products': products,
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

def all_main_categories(request):
    main_categories = MainCategory.objects.all()
    return render(request, 'main/all_main_categories.html', {
        'title': 'Главные категории',
        'menu': menu,
        'main_categories': main_categories
    })

def main_category_detail(request, custom_id):
    main_category = get_object_or_404(MainCategory, custom_id=custom_id)
    subcategories = main_category.subcategories.all()
    return render(request, 'main/main_category_detail.html', {
        'title': f"Главная категория: {main_category.name}",
        'menu': menu,
        'main_category': main_category,
        'subcategories': subcategories
    })

@login_required
@user_passes_test(is_admin)
def add_main_category(request):
    if request.method == 'POST':
        form = MainCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_main_categories')
    else:
        form = MainCategoryForm()
    return render(request, 'main/add_main_category.html', {
        'title': 'Добавить главную категорию',
        'menu': menu,
        'form': form
    })


@login_required
@user_passes_test(is_admin)
def edit_main_category(request, custom_id):
    main_category = get_object_or_404(MainCategory, custom_id=custom_id)

    if request.method == 'POST':
        form = MainCategoryForm(request.POST, request.FILES, instance=main_category)

        if form.is_valid():
            # Сохраняем изменения
            form.save()
            return redirect('main_category_detail', custom_id=main_category.custom_id)
    else:
        form = MainCategoryForm(instance=main_category)

    return render(request, 'main/edit_main_category.html', {
        'title': 'Редактировать главную категорию',
        'form': form
    })



@login_required
@user_passes_test(is_admin)
def delete_main_category(request, custom_id):
    main_category = get_object_or_404(MainCategory, custom_id=custom_id)
    if request.method == 'POST':
        main_category.delete()
        return redirect('all_main_categories')
    return render(request, 'main/delete_main_category.html', {
        'title': 'Удалить главную категорию',
        'main_category': main_category
    })


@login_required
@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_categories')
    else:
        form = CategoryForm()
    return render(request, 'main/add_category.html', {
        'title': 'Добавить категорию',
        'menu': menu,
        'form': form
    })


@login_required
@user_passes_test(is_admin)
def edit_category(request, custom_id):
    category = get_object_or_404(Category, custom_id=custom_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            # Проверяем уникальность custom_id для категории
            custom_id = form.cleaned_data['custom_id']
            if Category.objects.filter(custom_id=custom_id).exclude(pk=category.pk).exists():
                form.add_error('custom_id', 'Это кастомное ID уже существует для другой категории!')
            else:
                form.save()
                return redirect('category_detail', custom_id=category.custom_id)
    else:
        form = CategoryForm(instance=category)

    return render(request, 'main/edit_category.html', {
        'title': 'Редактировать категорию',
        'menu': menu,
        'form': form
    })


@login_required
@user_passes_test(is_admin)
def delete_category(request, custom_id):
    category = get_object_or_404(Category, custom_id=custom_id)
    if request.method == 'POST':
        category.delete()
        return redirect('all_categories')
    return render(request, 'main/delete_category.html', {
        'title': 'Удалить категорию',
        'menu': menu,
        'category': category
    })

@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ProductForm()
    return render(request, 'main/add_product.html', {
        'title': 'Добавить товар',
        'menu': menu,
        'form': form
    })


@login_required
@user_passes_test(is_admin)
def edit_product(request, custom_id):
    product = get_object_or_404(Product, custom_id=custom_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Проверяем уникальность custom_id для продукта
            custom_id = form.cleaned_data['custom_id']
            if Product.objects.filter(custom_id=custom_id).exclude(pk=product.pk).exists():
                form.add_error('custom_id', 'Это кастомное ID уже существует для другого товара!')
            else:
                form.save()
                return redirect('product_detail', custom_id=product.custom_id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'main/edit_product.html', {
        'title': 'Редактировать товар',
        'menu': menu,
        'form': form
    })


@login_required
@user_passes_test(is_admin)
def delete_product(request, custom_id):
    product = get_object_or_404(Product, custom_id=custom_id)
    if request.method == 'POST':
        product.delete()
        return redirect('catalog')
    return render(request, 'main/delete_product.html', {
        'title': 'Удалить товар',
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

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

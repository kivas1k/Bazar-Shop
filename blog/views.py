from django.shortcuts import render

menu = ["О нас", "Каталог", "Блог", "Акции", "Отзывы", "Контакты", "Войти"]

def blog_home(request):
    return render(request, 'blog/blog_home.html', {'title': 'Блог', 'menu': menu})

def blog_post(request, post_id):
    return render(request, 'blog/blog_post.html', {'title': 'Статья блога', 'menu': menu, 'post_id': post_id})

def blog_create(request):
    return render(request, 'blog/blog_create.html', {'title': 'Создать статью', 'menu': menu})

def blog_edit(request, post_id):
    return render(request, 'blog/blog_edit.html', {'title': 'Редактировать статью', 'menu': menu, 'post_id': post_id})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post
from .forms import PostForm

menu = ["О нас", "Каталог", "Блог", "Акции", "Отзывы", "Контакты", "Войти"]

def is_admin(user):
    return user.is_superuser

def blog_home(request):
    posts = Post.objects.all()
    return render(request, 'blog/blog_home.html', {'title': 'Блог', 'menu': menu, 'posts': posts})

def blog_post(request, custom_id):
    post = get_object_or_404(Post, custom_id=custom_id)
    return render(request, 'blog/blog_post.html', {'title': post.title, 'menu': menu, 'post': post})

@login_required
@user_passes_test(is_admin)
def blog_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_home')
    else:
        form = PostForm()
    return render(request, 'blog/blog_create.html', {'title': 'Создать статью', 'menu': menu, 'form': form})

@login_required
@user_passes_test(is_admin)
def blog_edit(request, custom_id):
    post = get_object_or_404(Post, custom_id=custom_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_post', custom_id=post.custom_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/blog_edit.html', {'title': 'Редактировать статью', 'menu': menu, 'form': form})

@login_required
@user_passes_test(is_admin)
def blog_delete(request, custom_id):
    post = get_object_or_404(Post, custom_id=custom_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_home')
    return render(request, 'blog/blog_delete.html', {'title': 'Удалить статью', 'menu': menu, 'post': post})
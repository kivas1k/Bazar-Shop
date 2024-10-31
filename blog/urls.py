from django.urls import path
from . import views

urlpatterns = [
#TODO все это
    path('', views.blog_home, name='blog_home'),                  # Главная страница блога
    path('post/<int:post_id>/', views.blog_post, name='blog_post'),  # Просмотр статьи
    path('post/new/', views.blog_create, name='blog_create'),        # Публикация новой статьи
    path('post/<int:post_id>/edit/', views.blog_edit, name='blog_edit'), # Редактирование статьи
]

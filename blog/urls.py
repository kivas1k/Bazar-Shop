from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('post/new/', views.blog_create, name='blog_create'),  # Создание нового поста
    path('post/<str:custom_id>/', views.blog_post, name='blog_post'),  # Отображение существующего поста
    path('post/<str:custom_id>/edit/', views.blog_edit, name='blog_edit'),  # Редактирование поста
    path('post/<str:custom_id>/delete/', views.blog_delete, name='blog_delete'),  # Удаление поста
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

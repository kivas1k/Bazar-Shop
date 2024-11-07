from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('post/<str:custom_id>/', views.blog_post, name='blog_post'),

    path('post/new/', views.blog_create, name='blog_create'),  # TODO

    path('post/<str:custom_id>/edit/', views.blog_edit, name='blog_edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

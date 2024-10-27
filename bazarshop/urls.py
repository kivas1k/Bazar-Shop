from django.contrib import admin
from django.urls import path, include
from main import views
from main.views import page_not_found


urlpatterns = [
    path('admin/', admin.site.urls),

    path('orders/', include('orders.urls')),
    path('users/', include('users.urls')),

    path('', include('main.urls')),
]

from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils.html import mark_safe  # Для отображения аватара как изображения
from django.conf import settings  # Для работы с медиафайлами

# Кастомизация отображения профиля пользователя в админке
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'avatar_thumbnail')  # Убираем 'user_comment'
    search_fields = ('user__username', 'user__email')  # Поиск по имени пользователя и email
    list_filter = ()  # Убираем фильтрацию по 'date_of_birth'

    # Метод для отображения аватара в виде картинки в списке
    def avatar_thumbnail(self, obj):
        if obj.avatar:
            # Убедитесь, что путь к изображению корректно строится, используя MEDIA_URL
            return mark_safe(f'<img src="{settings.MEDIA_URL}{obj.avatar.url}" width="50" height="50" />')
        return '-'
    avatar_thumbnail.short_description = 'Аватар'

# Регистрируем модель UserProfile в админке
admin.site.register(UserProfile, UserProfileAdmin)

# Также можно настроить отображение стандартных пользователей, если нужно
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')  # Настройка отображаемых полей
    search_fields = ('username', 'email')  # Поиск по полям
    list_filter = ('is_active', 'is_staff')  # Фильтрация по активности и ролям пользователя

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

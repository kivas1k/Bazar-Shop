from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils.html import mark_safe
from django.conf import settings

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'avatar_thumbnail')
    search_fields = ('user__username', 'user__email')
    list_filter = ()
    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{settings.MEDIA_URL}{obj.avatar.url}" width="50" height="50" />')
        return '-'
    avatar_thumbnail.short_description = 'Аватар'

admin.site.register(UserProfile, UserProfileAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

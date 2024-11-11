from django.contrib import admin
from django.utils.html import format_html
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'image_tag', 'custom_id')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Нет изображения"
    image_tag.short_description = 'Изображение'

    fields = ('custom_id', 'title', 'content', 'author', 'image')

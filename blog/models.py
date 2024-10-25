#TODO ПЕРЕДЕЛАТЬ ЕЩЕ 1000 РАЗ
from django.db import models
from django.contrib.auth.models import User

# Модель для постов в блоге
class BlogPost(models.Model):
    title = models.CharField(max_length=255)  # Заголовок поста (максимум 255 символов)
    content = models.TextField()  # Основное содержимое поста
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания поста (автоматически добавляется при создании)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Внешний ключ на пользователя, который является автором поста

    def __str__(self):
        return self.title  # Возвращает заголовок поста для удобного отображения

# Модель для комментариев к постам блога
class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  # Содержимое комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания комментария (автоматически добавляется)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'  # Возвращает строку с информацией о пользователе и посте

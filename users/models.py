#TODO ПЕРЕДЕЛАТЬ ЕЩЕ 1000 РАЗ
from django.db import models
from django.contrib.auth.models import User

# Модель профиля пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь один к одному с моделью User
    bio = models.TextField(blank=True)  # Биография пользователя (необязательное поле)
    avatar = models.ImageField(upload_to='avatars/', blank=True)  # Поле для загрузки аватара (необязательное)

    def __str__(self):
        return self.user.username  # Возвращает имя пользователя для лучшего представления

# Модель отзыва пользователя о продукте
class UserReview(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Рейтинг (целое число, например, от 1 до 5)
    comment = models.TextField()  # Текст отзыва

    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания отзыва

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"  # Возвращает строку с информацией о пользователе и продукте



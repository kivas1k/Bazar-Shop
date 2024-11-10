from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Category(models.Model):
    custom_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    pic_cat = models.ImageField(upload_to='categories/')
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pic_cat:
            img = Image.open(self.pic_cat.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.pic_cat.path)

class Product(models.Model):
    custom_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.picture:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.picture.path)

    @property
    def rating(self):
        likes = self.ratings.filter(is_like=True).count()
        dislikes = self.ratings.filter(is_like=False).count()
        return likes - dislikes

class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.username} - {'Like' if self.is_like else 'Dislike'} on {self.product.name}"

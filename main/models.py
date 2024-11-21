from django.db import models
from django.core.validators import MinValueValidator
from PIL import Image

class MainCategory(models.Model):
    custom_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    picture = models.ImageField(upload_to='main_categories/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.picture:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.picture.path)



class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories')
    custom_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.picture:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.picture.path)


class Product(models.Model):
    custom_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
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

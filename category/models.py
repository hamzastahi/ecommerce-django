from django.db import models

# Create your models here.
class Category(models.Model):
    
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    images = models.ImageField(upload_to='photos/categories')

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name
from django.db import models
from django.contrib.auth import get_user_model
from category_api.models import Category

UserModel = get_user_model()

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title

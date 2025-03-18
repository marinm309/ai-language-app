from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/', null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

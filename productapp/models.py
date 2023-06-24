from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=60)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)


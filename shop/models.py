from django.db import models
from decimal import Decimal

class Product(models.Model):
    class RatingChoice(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    discounted_price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
from django.db import models
from django.contrib.auth.models import User

# Product model
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('fruits', 'Fruits'),
        ('vegetables', 'Vegetables'),
        ('spices', 'Spices'),
        ('flowers', 'Flowers'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    added_by = models.CharField(max_length=100,default="UnKnown")

    def __str__(self):
        return f"{self.name} ({self.category}) - {self.seller.username}"

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    seller_name = models.CharField(max_length=255, default="Unknown Seller")
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, default="Pending") 

    def __str__(self):
        return f"Order {self.id} - {self.buyer.username}"


class PageBackground(models.Model):
    page_name = models.CharField(max_length=255, unique=True)
    background_image = models.ImageField(upload_to="backgrounds/")

    def __str__(self):
        return self.page_name
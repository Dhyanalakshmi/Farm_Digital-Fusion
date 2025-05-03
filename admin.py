from django.contrib import admin
from .models import Product, Order
from .models import PageBackground

admin.site.register(PageBackground)
admin.site.register(Product)
admin.site.register(Order)

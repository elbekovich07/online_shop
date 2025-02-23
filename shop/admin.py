from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discounted_price', 'updated_at')
    list_filter = ('updated_at', 'price')
    search_fields = ('name', 'description')
    ordering = ('-updated_at',)

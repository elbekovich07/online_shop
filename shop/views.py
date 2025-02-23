from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Bazadan mahsulot olish
    related_products = Product.objects.exclude(id=product_id)[:4]  # 4 ta boshqa mahsulot

    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop/detail.html', context)

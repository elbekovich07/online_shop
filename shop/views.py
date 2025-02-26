from django.shortcuts import render, get_object_or_404
from .models import Product , Category

def index(request):
    products = Product.objects.all().order_by('-updated_at')
    context = {
        'products': products
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }

    return render(request, 'shop/detail.html', context)

def all_products(request):
    products = Product.objects.all().order_by('-updated_at')
    context = {
        'products': products
    }
    return render(request, 'shop/home.html', context)



def home(request):
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {'categories': categories})


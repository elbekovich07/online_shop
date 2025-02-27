from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from shop.forms import ProductForm
from shop.models import Product, Category


# Create your views here.


def index(request, category_id: int | None = None):
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all().order_by('-updated_at')
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'shop/detail.html', context)



@login_required(login_url='/admin/')
def product_create(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)

            return redirect('index')

    context = {
        'form': form
    }

    return render(request, 'shop/add-product.html', context)



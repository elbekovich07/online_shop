from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from shop.models import Product, Category
from shop.forms import ProductForm


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
            product = form.save(commit=False)
            product.save()

            return redirect('index')

    context = {
        'form': form
    }
    return render(request, 'shop/add-product.html', context)


@login_required(login_url='/admin/')
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('index')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form
    }
    return render(request, 'shop/edit-product.html', context)




@login_required(login_url='/admin/')
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('index')



def product_list(request, filter_by=None):
    products = Product.objects.all()

    if filter_by ==  'Likes':
        products = products.order_by('-Likes')
    elif filter_by == 'Expensive':
        products = products.order_by('-price')
    elif filter_by == 'Cheap':
        products = products.order_by('price')

    context = {
        'products': products,
    }
    return render(request, 'shop/home.html', context)





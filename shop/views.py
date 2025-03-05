from tkinter.font import names

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from shop.forms import ProductModelForm, CommentModelForm
from shop.models import Product, Category


# Create your views here.


def index(request, category_id: int | None = None):
    search_query = request.GET.get('q', '')
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all().order_by('-updated_at')
    if search_query:
        products = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments.all()
    context = {
        'product': product,
        'categories': categories,
        'comments': comments
    }
    return render(request, 'shop/detail.html', context)


@login_required(login_url='/admin/')
def product_create(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()

            return redirect('index')

    context = {
        'form': form,
        'action': 'Create'
    }
    return render(request, 'shop/add-product.html', context)


@login_required(login_url='/admin/')
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('index')
    else:
        form = ProductModelForm(instance=product)

    context = {
        'product': product,
        'form': form,
        'action': 'Update'
    }
    return render(request, 'shop/edit-product.html', context)


@login_required(login_url='/admin/')
def product_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    if product:
        product.delete()
        return redirect('index')
    return render(request, 'shop/detail.html', {'product': product})


def product_list(request, filter_by=None):
    products = Product.objects.all()

    if filter_by and filter_by.lower() == 'likes':
        products = products.order_by('-likes')
    elif filter_by == 'Expensive':
        products = products.order_by('-price')
    elif filter_by == 'Cheap':
        products = products.order_by('price')

    context = {
        'products': products,
    }
    return render(request, 'shop/home.html', context)


@login_required(login_url='/admin/')
def product_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.likes += 1
        product.save()
        return JsonResponse({'likes': product.likes})


def comment_view(request, pk):
    product = Product.objects.get(id=pk)
    form = CommentModelForm()
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            rating = request.POST.get('rating')
            print(type(rating))
            comment.rating = rating
            comment.product = product
            comment.save()
            return redirect('product_detail', product.id)

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'shop/detail.html', context)


def place_order(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        if not name or not phone:
            messages.error(request, "Iltimos, ism va telefon raqamni kiriting.")
            return redirect('product_detail', product_id=product.id)

        if product.quantity > 0:
            product.quantity -= 1
            product.save()
            messages.success(request, "Buyurtma muvaffaqiyatli amalga oshirildi!")
        else:
            messages.error(request, "Mahsulot tugagan!")

        return redirect('product_detail', product_id=product.id)
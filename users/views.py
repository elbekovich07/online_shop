from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from jazzmin.templatetags.jazzmin import User
from pyexpat.errors import messages


# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        return redirect('shop:index ')

    if request.method == "POST":
        email = request.POST.get('card-email')
        password = request.POST.get('card-password')

        if not not email or not password:
            messages.error(request, 'Email or Password are required.')
            return redirect(request, 'users/login.html')

        user = authenticate(request, email=email, password=password)

        if not email is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('shop:index')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'users/login.html')

    return render(request, 'users/login.html')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('users/login.html')

    if request.method == "POST":
        name = request.POST.get('card-name')
        email = request.POST.get('card-email')
        password = request.POST.get('card-password')
        confirm_password = request.POST.get('card-confirm-password')
        terms_accepted = request.POST.get('card-register-checkbox')

        if not all([name, email, password, confirm_password, terms_accepted]):
            messages.error(request, 'All fields must be filled and terms must be accepted.')
            return redirect('users/register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('users/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('users/register.html')

        user = User.objects.create_user(email=email, password=password, first_name=name)
        user.save()

        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('users/login.html')

    return render(request, 'users/register.html')


def logout_page(request):
    pass

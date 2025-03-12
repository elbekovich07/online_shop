from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        return redirect('shop:index')

    if request.method == "POST":
        email = request.POST.get('card-email')
        password = request.POST.get('card-password')

        if not email or not password:
            messages.error(request, 'Email or Password is required.')
            return redirect('users:login_page')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, 'Succesfully logged in!')
            return redirect('shop:index')
        else:
            messages.error(request, 'Email or Password is incorrect.')
            return render(request, 'users/login.html')

    return render(request, 'users/login.html')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('shop:index')

    if request.method == "POST":
        name = request.POST.get('card-name')
        email = request.POST.get('card-email')
        password = request.POST.get('card-password')
        confirm_password = request.POST.get('card-confirm-password')
        terms_accepted = request.POST.get('card-register-checkbox')

        if not all([name, email, password, confirm_password, terms_accepted]):
            messages.error(request, 'All fields must be filled, and terms must be accepted.')
            return redirect('users:register_page')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('users:register_page')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return redirect('users:register_page')

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()

        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('users:login_page')

    return render(request, 'users/register.html')


def logout_page(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('users:login_page')
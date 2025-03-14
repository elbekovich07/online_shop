from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from users.forms import LoginForm, RegisterForm
from .models import CustomUser


# Create your views here.


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('shop:index')
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'Disabled account'
                    )
                    return render(request, 'users/login.html')
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Username or Password invalid'
                )
                return render(request, 'users/login.html')

    return render(request, 'users/login.html', {'form': form})


def register_page(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('shop:index')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')

    return render(request, 'users/register.html', {'form': form})


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('shop:index')
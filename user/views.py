from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, redirect


def register(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password1 = request.POST.get("pass1")
        password2 = request.POST.get("pass2")

        if not all([name, email, password1, password2]):
            messages.error(request, "Все поля обязательный для заполнения")
            return render(request, "user/register.html")

        if password1 != password2:
            messages.error(request, "Пароли не совпадают")
            return render(request, "user/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с такой почтой уже существует")
            return render(request, "user/register.html")

        try:
            User.objects.create(
                username=name,
                email=email,
                password=make_password(password1)
            )

            return redirect("/login")
        except Exception as e:
            messages.error(request, f"Ошибка на сервере: {str(e)}")


    return render(request, "user/register.html")


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('pass1')

        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            messages.error(request, "Неверная электронная почта или пароль")

    return render(request, 'user/login.html', {'messages': messages.get_messages(request)})


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("/login")


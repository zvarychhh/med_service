from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import MyUserCreationForm, MyLoginForm


# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
            return redirect("home")
    else:
        form = MyUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = MyLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Ви увійшли!")
                return redirect("home")
            else:
                messages.error(request, "Неправильно введено пароль або логін.")
    else:
        form = MyLoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")

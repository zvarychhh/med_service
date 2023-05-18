from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from patient.forms import PatientCreationForm
from doctors.forms import DoctorCreationForm
from uuid import uuid4

from .forms import EmailForm, PasswordForm, LoginForm
from .models import MyUser
from .reset import send_password_email
from django.utils.translation import activate

activate("ua")


def registration_view(request):
    if request.method == "POST":
        form = PatientCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
            return redirect("home")
    else:
        form = PatientCreationForm()
    return render(request, "registration/registration.html", {"form": form})


def doc_registration_view(request):
    if request.method == "POST":
        form = DoctorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
            return redirect("home")
    else:
        form = DoctorCreationForm()
    return render(request, "registration/doc_registration.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
        messages.error(request, "Неправильно введено пароль або пошту.")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


# Password reset views


def reset_password(request):
    context = {"form": EmailForm}
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            user = MyUser.objects.filter(email=email).first()

            if not user:
                messages.error(request, "Користувача з такою поштою не виявлено.")
                return render(request, "reset_password/email_check.html", context)

            uid = uuid4()
            user.forget_password_token = uid
            user.save()
            title = "Лінк для зміни паролю"
            message = f"Доброго дня, {user}" \
                      f", для відновлення паролю " \
                      f"перейдіть за посиланням " \
                      f"http://127.0.0.1:8000/user/change_password/{uid} "

            send_password_email(user, title, message)
            messages.success(request, "Посилання для скидання паролю було відправлене на пошту.")
            context["user_id"] = user.pk
            return render(request, "reset_password/email_check.html", context)
    except Exception as e:
        messages.error(request, str(e))

    return render(request, "reset_password/email_check.html", context)


def change_password(request, token):
    context = {"form": PasswordForm}
    try:
        if request.method == "POST":
            user = MyUser.objects.filter(forget_password_token=token).first()
            if not user:
                context["error_msg"] = "Посилання не дійсне."
                return render(request, "reset_password/change_password.html", context)
            form = PasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get("password")
                confirm_password = form.cleaned_data.get("confirm_password")
                if password != confirm_password:
                    context["error_msg"] = "Паролі не співпадають."
                    return render(
                        request, "reset_password/change_password.html", context
                    )
                user.set_password(password)
                user.forget_password_token = ""
                user.save()
                context = {
                    "success_msg": "Пароль успішно змінено",
                    "form": PatientLoginForm(),
                }
                return redirect("login")

    except Exception as e:
        print(e)
    return render(request, "reset_password/change_password.html", context)

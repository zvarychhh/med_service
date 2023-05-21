from django.shortcuts import render, redirect
from doctors.models import DoctorProfile, Specialty
from myuser.models import Mailing
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db import IntegrityError

from django.core.mail import send_mail
from django.conf import settings
import phonenumbers


def index(request):
    if request.GET:
        email = request.GET.get("email")
        try:
            validate_email(email)
            Mailing(email=email).save()
            messages.success(request, "Пошта була успішно додана.")
        except ValidationError:
            messages.error(request, "Невірно введено електронну пошту")
        except IntegrityError:
            messages.warning(request, "Дана пошта вже була додана")
    context = {
        "doctors": DoctorProfile.objects.all(),
        "specialties": Specialty.objects.all(),
    }
    return render(request, "home/index.html", context)


def about(request):
    if request.GET:
        name = request.GET.get("name")
        phone_number = request.GET.get("phone")
        try:
            phone = phonenumbers.parse(phone_number, "UA")
            if phonenumbers.is_valid_number(phone):
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [settings.EMAIL_HOST_USER]
                send_mail(f"Дзвінок, {name} --- {phone_number}", f"Ім'я: {name}\nНомер телефону: {phone_number}",
                          email_from,
                          recipient_list)
                messages.success(request, "Ваш запит успішно прийнято.")
            else:
                messages.error(request, "Номер введено невірно.")
        except:
            messages.error(request, "Номер введено невірно.")
        return redirect("about")
    return render(request, "home/about.html")

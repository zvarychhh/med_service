from django.shortcuts import render
from doctors.models import DoctorProfile, Specialty
from myuser.models import Mailing
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db import IntegrityError


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
    return render(request, "home/about.html")

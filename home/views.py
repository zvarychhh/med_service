from django.shortcuts import render
from django.http import HttpResponse
from doctors.models import DoctorProfile, Specialty


def index(request):
    context = {
        "doctors": DoctorProfile.objects.all(),
        "specialties": Specialty.objects.all(),
    }
    return render(request, "home/index.html", context)


def about(request):
    return render(request, "home/about.html")

from django.db.models import Q
from .models import Doctor, Specialty
from django.shortcuts import render, redirect


def doctor_list(request):
    doctors = Doctor.objects.all()
    specialties = Specialty.objects.all()
    query = request.GET.get("q")
    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)
        )
    specialty_filter = request.GET.get("specialty")
    if specialty_filter:
        doctors = doctors.filter(specialty__id=specialty_filter)
    return render(
        request, "doctors/index.html", {"doctors": doctors, "specialties": specialties}
    )

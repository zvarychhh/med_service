from datetime import datetime

from django.shortcuts import render
from .models import PatientProfile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from doctors.models import Appointment


# Create your views here.

def patient_appointment(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role == "DOCTOR":
        return redirect("doctor_appointment")
    if request.user.role == "ADMIN":
        messages.warning(request, "Ця секція для лікарів та пацієнтів.")
        return redirect("home")

    patient = PatientProfile.objects.get(user=request.user)
    if request.POST:
        appointment_id = request.POST.get("appointment_id")
        appointment = Appointment.objects.get(pk=appointment_id)
        appointment.patient = None
        appointment.save()
        messages.success(request, "Запис до лікаря було видалено.")
        return redirect("patient_appointment")

    appointments = Appointment.objects.filter(patient=patient).order_by("-starttime")
    paginator = Paginator(appointments, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "now": datetime.now()}
    return render(request, "patient/patient_appointment.html", context)

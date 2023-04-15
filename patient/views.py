from datetime import datetime

from django.shortcuts import render
from .models import PatientProfile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from doctors.models import Appointment


# Create your views here.

def patient_appointment(request):
    if not request.user.id:
        return redirect("login")
    if request.user.role != "PATIENT":
        return redirect("login")
    patient = PatientProfile.objects.get(user=request.user)
    if request.POST:
        appointment_id = request.POST.get("appointment_id")
        appointment = Appointment.objects.get(pk=appointment_id)
        appointment.patient = None
        appointment.save()
        messages.success(request, "Запис до лікаря було видалено.")
        return redirect("patient_appointment")

    appointments = Appointment.objects.filter(patient=patient).order_by("-starttime")
    for i in appointments:
        if i.starttime < datetime.now():
            i.flag = False
            i.save()
    context = {"appointments": appointments}
    return render(request, "patient/patient_appointment.html", context)

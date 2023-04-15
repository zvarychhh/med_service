from django.db.models import Q
from .models import DoctorProfile, Specialty, Appointment
from django.shortcuts import render, redirect
from django.contrib import messages
from patient.models import PatientProfile
from .models import Appointment
import datetime
import locale


def doctor_list(request):
    doctors = DoctorProfile.objects.all()
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


def get_days(pk):
    doc = DoctorProfile.objects.get(pk=pk)
    appointments = Appointment.objects.filter(doctor=doc).order_by("starttime")
    days = {}
    locale.setlocale(locale.LC_TIME, "uk_UA.utf8")

    for appointment in appointments:
        if appointment.starttime > datetime.datetime.now().replace():
            day = datetime.date.strftime(appointment.starttime, "%d.%m.%y")
            verb_day = datetime.date.strftime(appointment.starttime, "%A").capitalize()
            days.setdefault((day, verb_day), []).append(
                [appointment.starttime.time().strftime("%H:%M"), appointment.endtime.time().strftime("%H:%M"),
                 appointment.patient, f"{appointment.pk}"])
    return days


def doctor_visit(request, pk):
    doc = DoctorProfile.objects.get(pk=pk)

    if request.method == "GET" and request.GET.get("appointment_id"):
        patient = PatientProfile.objects.filter(user_id=request.user.pk)
        if not patient:
            messages.warning(request, 'Для запису потрібно увійти як пацієнт.')
            return redirect("doctors")
        patient = PatientProfile.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient, doctor_id=pk)
        # Перевірка чи в користувача вже є запланована зустріч до цього лікаря
        for i in appointments:
            if datetime.datetime.now() < i.starttime:
                messages.warning(request, "У вас вже є запис до цього лікаря.")
                return redirect("doctor_visit", pk=pk)

        appointment_id = request.GET.get("appointment_id")
        appointment = Appointment.objects.get(pk=appointment_id)
        patient = PatientProfile.objects.get(user=request.user)
        appointment.patient = patient
        appointment.save()
        messages.success(request, 'Запис успішно створено.')
    days = get_days(pk)

    context = {"doctor": doc,
               "date": days}

    return render(request, "doctors/doctor.html", context)


def doctor_appointment(request):
    if not request.user.id:
        return redirect("home")
    if request.user.role != "DOCTOR":
        return redirect("home")
    doctor = DoctorProfile.objects.get(user=request.user.pk)
    appointment = Appointment.objects.filter(doctor=doctor)
    return render(request, "doctors/appointment.html", {"appointment": appointment})

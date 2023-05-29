from django.contrib import admin
from .models import DoctorProfile, Specialty, Appointment, AppointmentManage

admin.site.register(DoctorProfile)
admin.site.register(Specialty)
admin.site.register(Appointment)
admin.site.register(AppointmentManage)

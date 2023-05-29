from django.urls import path
from .views import doctor_list, doctor_visit, doctor_appointment

urlpatterns = [
    path("appointment/", doctor_appointment, name="doctor_appointment"),
    path("", doctor_list, name="doctors"),
    path("<pk>/", doctor_visit, name="doctor_visit"),

]

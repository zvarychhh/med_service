from django.urls import path
from .views import patient_appointment

urlpatterns = [
    path("appointment/", patient_appointment, name="patient_appointment")

]

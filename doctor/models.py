from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from phone_field import PhoneField

from myuser.models import MyUser, MyUserManager
from patient.models import PatientProfile
from datetime import timedelta, datetime


class Specialty(models.Model):
    specialty = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.specialty


class DoctorManager(MyUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super.get_queryset(*args, **kwargs)
        return results.filter(role=MyUser.Role.DOCTOR)


class Doctor(MyUser):
    base_role = MyUser.Role.DOCTOR
    doctor = DoctorManager()

    class Meta:
        proxy = True

    def __str__(self):
        return f"{self.base_role} {self.pk}"


@receiver(post_save, sender=Doctor)
def create_patient_profile(sender, instance, created, **kwargs):
    if created and instance.role == "DOCTOR":
        DoctorProfile.objects.create(user=instance)


class DoctorProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)

    specialty = models.ForeignKey(
        Specialty, on_delete=models.CASCADE, blank=True, null=True
    )
    door_number = models.IntegerField(null=True, blank=True, unique=True)
    phone_number = PhoneField(null=True, blank=True, default="")
    experience = models.IntegerField(null=True, blank=True)
    photo = models.ImageField(upload_to=f"doctor_photos/", blank=True)
    confirmation = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Appointment(models.Model):
    doctor = models.ForeignKey("DoctorProfile", on_delete=models.CASCADE)
    appointmentManage = models.ForeignKey("AppointmentManage", on_delete=models.CASCADE, null=True, blank=True)
    starttime = models.DateTimeField(null=True)
    endtime = models.DateTimeField(null=True)
    patient = models.ForeignKey("patient.PatientProfile", default=None,
                                on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.doctor.user.last_name} {self.starttime.date()} ( {self.starttime.time().strftime('%H:%M')} " \
               f"- {self.endtime.time().strftime('%H:%M')})"


class AppointmentManage(models.Model):
    doctor = models.ForeignKey("DoctorProfile", on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    appointment_time = models.IntegerField(default=30)
    break_time = models.IntegerField(default=0)

    def __str__(self):
        return f'Записи до {self.doctor} з {self.start_time.strftime("%Y-%m-%d : %H:%M")}.'


@receiver(post_save, sender=AppointmentManage)
def create_appointment(sender, instance, created, **kwargs):
    if created and instance.doctor:
        doctor = instance.doctor
        start = instance.start_time
        end = instance.end_time
        minute = instance.appointment_time
        break_time = instance.break_time

        while start + timedelta(minutes=(minute + break_time)) < end:
            temp_end = start + timedelta(minutes=minute)
            Appointment.objects.create(doctor=doctor, starttime=start, endtime=temp_end, appointmentManage=instance)
            start = start + timedelta(minutes=(minute + break_time))

        for i in Appointment.objects.filter(doctor=doctor):
            if i.starttime < datetime.now() and not i.patient:
                i.delete()

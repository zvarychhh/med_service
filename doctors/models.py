from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from myuser.models import MyUser, MyUserManager


class Specialty(models.Model):
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.specialty


class DoctorManager(MyUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super.get_queryset(*args, **kwargs)
        return results.filter(role=MyUser.Role.DOCTOR)


class Doctor(MyUser):
    base_role = MyUser.Role.DOCTOR
    patient = DoctorManager()

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
    doctor_id = models.IntegerField(blank=True, null=True)

    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, blank=True)
    descriptions = models.TextField(blank=True)
    star_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(f"doctor_photos/", blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from myuser.models import MyUser, MyUserManager


class PatientManager(MyUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super.get_queryset(*args, **kwargs)
        return results.filter(role=MyUser.Role.PATIENT)


class Patient(MyUser):
    base_role = MyUser.Role.PATIENT

    patient = PatientManager()

    class Meta:
        proxy = True

    def __str__(self):
        return f"{self.base_role} {self.pk}"


@receiver(post_save, sender=Patient)
def create_patient_profile(sender, instance, created, **kwargs):
    if created and instance.role == "PATIENT":
        PatientProfile.objects.create(user=instance)


class PatientProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    doctor_id = models.IntegerField(blank=True, null=True)

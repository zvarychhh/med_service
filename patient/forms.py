from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Patient


class PatientCreationForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "blood_type",
            "date_of_birth",
            "gender",
        ]

    def save(self, commit=True):
        user = super(PatientCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

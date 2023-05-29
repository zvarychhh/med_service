from .models import Doctor
from django.contrib.auth.forms import UserCreationForm


class DoctorCreationForm(UserCreationForm):
    class Meta:
        model = Doctor
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "date_of_birth",
            "gender",
        ]

    def save(self, commit=True):
        user = super(DoctorCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

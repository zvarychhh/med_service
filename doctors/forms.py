from django import forms


class AppointmentForm(forms.Form):
    id = forms.IntegerField()

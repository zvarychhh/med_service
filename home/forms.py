from django import forms

from myuser.models import MyUser


class MailingForm(forms.Form):
    class Meta:
        model = MyUser

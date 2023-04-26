from django.core.mail import send_mail
from django.conf import settings


def send_password_email(user, title, message):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(title, message, email_from, recipient_list)
    return True

from django.core.mail import send_mail
from django.conf import settings


def send_password_email(user, token):
    subject = "Лінк для зміни паролю"
    message = f"Доброго дня, {user}, для відновлення паролю перейдіть за посиланням http://127.0.0.1:8000/user/change_password/{token} "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)
    return True

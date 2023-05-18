from django.urls import path
from .views import (
    registration_view,
    login_view,
    logout_view,
    reset_password,
    change_password,
    doc_registration_view,
)

urlpatterns = [
    path("registration/", registration_view, name="registration"),
    path("doc_registration/", doc_registration_view, name="doc_registration"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("reset_password/", reset_password, name="reset_password"),
    path("change_password/<token>/", change_password, name="change_password"),
]

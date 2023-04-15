from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    reset_password,
    change_password,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("reset_password/", reset_password, name="reset_password"),
    path("change_password/<token>/", change_password, name="change_password"),
]

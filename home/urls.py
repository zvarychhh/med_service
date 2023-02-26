from django.urls import path
from .views import index, about, services

urlpatterns = [
    path("", index, name="home"),
    path("about/", about, name="about"),
    path("services/", services, name="services"),
]

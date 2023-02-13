from django.urls import path
from .views import index, about, login, services


urlpatterns = [
    path('', index, name='home'),
    path('about/',about, name='about' ),
    path('login/',login, name='login'),
    path('services/',services, name='services' ),
]

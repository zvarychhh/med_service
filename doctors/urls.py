from django.urls import path
from .views import doctor_list, register_view, login_view, logout_view

urlpatterns = [
    path('', doctor_list, name='doctors'),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name='logout')

]

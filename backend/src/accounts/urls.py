# accounts/urls.py
from django.urls import path
from .views.auth_views import UserRegistrationView, UserLoginView, change_password, campus_view

#Definicion de rutas para la app accounts
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),  #Ruta para el registro de usuario
    path('login/', UserLoginView.as_view(), name='login'),               #Ruta para el inicio de sesion
    path('change_password/', change_password, name='change_password'),   #Ruta para cambair la contraseña
    path('campus/', campus_view, name='campus'),                         #Ruta para acceder al campus
]

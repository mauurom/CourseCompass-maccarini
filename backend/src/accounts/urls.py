# accounts/urls.py
from django.urls import path
from .views.auth_views import UserRegistrationView, UserLoginView, change_password, campus_view

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('change_password/', change_password, name='change_password'),
    path('campus/', campus_view, name='campus'),
]

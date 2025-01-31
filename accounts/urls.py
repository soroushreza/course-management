from django.urls import path
from .views import (
    StudentRegistrationView,
    StudentLoginView,
    PasswordResetView,
    LogoutView
)

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='register'),
    path('login/', StudentLoginView.as_view(), name='login'),
]
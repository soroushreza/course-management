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
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('logout/',LogoutView.as_view(),name='logout'),
]

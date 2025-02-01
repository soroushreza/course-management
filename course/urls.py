from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('profile/', views.StudentProfileView.as_view(), name='student_profile'),
    path('profile/edit/', views.StudentProfileEditView.as_view(), name='student_profile_edit'),

]


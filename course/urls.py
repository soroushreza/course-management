from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('profile/', views.StudentProfileView.as_view(), name='student_profile'),
    path('profile/edit/', views.StudentProfileEditView.as_view(), name='student_profile_edit'),
    path('course-selection/', views.course_selection_view, name='course_selection'),
    path('drop-course/', views.drop_course, name='drop_course'),
    path('get-enrolled-courses/', views.get_enrolled_courses, name='get_enrolled_courses'),
    path('enroll-course/', views.enroll_course, name='enroll_course'),
    path('get-department-courses/', views.get_department_courses, name='get_department_courses'),
    path('weekly-schedule/', views.weekly_schedule_view, name='weekly_schedule'),

]


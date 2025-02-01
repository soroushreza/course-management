# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('management/courses/report/', views.course_reports, name='course_report'),
    
    # URL‌های مدیریت زمان‌بندی دروس
    path('management/courses/<int:course_id>/add-schedule/', views.add_course_schedule, name='add_course_schedule'),
    path('management/courses/schedule/edit/<int:schedule_id>/', views.edit_course_schedule, name='edit_course_schedule'),
    path('management/courses/schedule/delete/<int:schedule_id>/', views.delete_course_schedule, name='delete_course_schedule'),

]
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('management/courses/report/', views.course_reports, name='course_report'),
    path('management/courses/', views.admin_course_management, name='admin_course_management'),
    path('management/courses/add/', views.add_course, name='add_course'),
    path('management/courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('management/courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('management/courses/detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enrollment/<int:enrollment_id>/delete/', views.delete_enrollment, name='delete_enrollment'),
    
    # URL‌های مدیریت زمان‌بندی دروس
    path('management/courses/<int:course_id>/add-schedule/', views.add_course_schedule, name='add_course_schedule'),
    path('management/courses/schedule/edit/<int:schedule_id>/', views.edit_course_schedule, name='edit_course_schedule'),
    path('management/courses/schedule/delete/<int:schedule_id>/', views.delete_course_schedule, name='delete_course_schedule'),

    # URLs مدیریت پیش‌نیاز و هم‌نیاز
    path('course/<int:course_id>/add-prerequisite/', views.add_prerequisite, name='add_prerequisite'),
    path('prerequisite/<int:prerequisite_id>/delete/', views.delete_prerequisite, name='delete_prerequisite'),
    path('course/<int:course_id>/add-corequisite/', views.add_corequisite, name='add_corequisite'),
    path('corequisite/<int:corequisite_id>/delete/', views.delete_corequisite, name='delete_corequisite'),
    
    # URLs مدیریت کاربران
    path('users/', views.user_management, name='user_management'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/<int:student_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:student_id>/delete/', views.delete_user, name='delete_user'),
        
    path('course/<int:course_id>/add-classroom/', views.add_course_classroom, name='add_course_classroom'),
    path('course-classroom/<int:course_classroom_id>/delete/', views.delete_course_classroom, name='delete_course_classroom'),
]
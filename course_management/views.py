# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from accounts.models import Student
from course.models import Course, CourseClassroom, CourseSchedule, Prerequisite, Corequisite, Enrollment
from .forms import (
    CourseClassroomForm,
    CourseForm,
    CourseScheduleForm,
    CustomUserForm,
    PrerequisiteForm,
    CorequisiteForm,
    StudentForm,
)
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .forms import CourseForm, CourseScheduleForm


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def add_course_schedule(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.course = course
            schedule.save()
            messages.success(request, "زمان‌بندی درس با موفقیت اضافه شد.")
            return redirect("course_detail", course_id=course.id)
    else:
        form = CourseScheduleForm()
    return render(
        request,
        "course_management/add_course_schedule.html",
        {"form": form, "course": course},
    )


@user_passes_test(is_admin)
def edit_course_schedule(request, schedule_id):
    schedule = get_object_or_404(CourseSchedule, id=schedule_id)
    if request.method == "POST":
        form = CourseScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, "زمان‌بندی درس با موفقیت ویرایش شد.")
            return redirect("course_detail", course_id=schedule.course.id)
    else:
        form = CourseScheduleForm(instance=schedule)
    return render(
        request,
        "course_management/edit_course_schedule.html",
        {"form": form, "schedule": schedule},
    )


@user_passes_test(is_admin)
def delete_course_schedule(request, schedule_id):
    schedule = get_object_or_404(CourseSchedule, id=schedule_id)
    course_id = schedule.course.id
    if request.method == "POST":
        schedule.delete()
        messages.success(request, "زمان‌بندی درس با موفقیت حذف شد.")
        return redirect("course_detail", course_id=course_id)
    return render(
        request, "course_management/delete_course_schedule.html", {"schedule": schedule}
    )


@user_passes_test(is_admin)
def course_reports(request):
    courses = Course.objects.all()
    course_data = []
    for course in courses:
        enrollments = Enrollment.objects.filter(
            course=course, 
            status="approved"
        ).select_related('student__user')
        
        course_data.append({
            "name": course.name,
            "enrolled_students": enrollments.count(),
            "capacity": course.capacity,
            "initial_capacity": course.initial_capacity,
            "enrollments": enrollments,  
            "id": course.id
        })
    return render(
        request, "course_management/course_reports.html", {"course_data": course_data}
    )

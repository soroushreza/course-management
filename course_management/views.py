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

@user_passes_test(is_admin)
def delete_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == "POST":
        enrollment.delete()
        messages.success(request, "ثبت نام دانشجو با موفقیت حذف شد.")
        return redirect("course_report")
    return render(
        request, 
        "course_management/delete_enrollment.html", 
        {"enrollment": enrollment}
    )


@user_passes_test(is_admin)
def admin_course_management(request):
    courses = Course.objects.all()
    return render(
        request, "course_management/admin_course_management.html", {"courses": courses}
    )


@user_passes_test(is_admin)
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "درس با موفقیت اضافه شد.")
            return redirect("admin_course_management")
    else:
        form = CourseForm()
    return render(request, "course_management/add_course.html", {"form": form})


@user_passes_test(is_admin)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "درس با موفقیت ویرایش شد.")
            return redirect("admin_course_management")
    else:
        form = CourseForm(instance=course)
    return render(request, "course_management/edit_course.html", {"form": form})


@user_passes_test(is_admin)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        messages.success(request, "درس با موفقیت حذف شد.")
        return redirect("admin_course_management")
    return render(request, "course_management/delete_course.html", {"course": course})


@user_passes_test(is_admin)
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    schedules = CourseSchedule.objects.filter(course=course)
    prerequisites = Prerequisite.objects.filter(course=course)
    corequisites = Corequisite.objects.filter(course=course)
    return render(
        request,
        "course_management/course_detail.html",
        {
            "course": course,
            "schedules": schedules,
            "prerequisites": prerequisites,
            "corequisites": corequisites,
        },
    )


@user_passes_test(is_admin)
def add_prerequisite(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = PrerequisiteForm(request.POST)
        if form.is_valid():
            prerequisite = form.save(commit=False)
            prerequisite.course = course
            prerequisite.save()
            messages.success(request, "پیش‌نیاز با موفقیت اضافه شد.")
            return redirect("course_detail", course_id=course.id)
    else:
        form = PrerequisiteForm(initial={"course": course})
    return render(
        request,
        "course_management/add_prerequisite.html",
        {"form": form, "course": course},
    )


@user_passes_test(is_admin)
def delete_prerequisite(request, prerequisite_id):
    prerequisite = get_object_or_404(Prerequisite, id=prerequisite_id)
    course_id = prerequisite.course.id
    if request.method == "POST":
        prerequisite.delete()
        messages.success(request, "پیش‌نیاز با موفقیت حذف شد.")
        return redirect("course_detail", course_id=course_id)
    return render(
        request,
        "course_management/delete_prerequisite.html",
        {"prerequisite": prerequisite},
    )


@user_passes_test(is_admin)
def add_corequisite(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CorequisiteForm(request.POST)
        if form.is_valid():
            corequisite = form.save(commit=False)
            corequisite.course = course
            corequisite.save()
            messages.success(request, "هم‌نیاز با موفقیت اضافه شد.")
            return redirect("course_detail", course_id=course.id)
    else:
        form = CorequisiteForm(initial={"course": course})
    return render(
        request,
        "course_management/add_corequisite.html",
        {"form": form, "course": course},
    )


@user_passes_test(is_admin)
def delete_corequisite(request, corequisite_id):
    corequisite = get_object_or_404(Corequisite, id=corequisite_id)
    course_id = corequisite.course.id
    if request.method == "POST":
        corequisite.delete()
        messages.success(request, "هم‌نیاز با موفقیت حذف شد.")
        return redirect("course_detail", course_id=course_id)
    return render(
        request,
        "course_management/delete_corequisite.html",
        {"corequisite": corequisite},
    )


@user_passes_test(is_admin)
def user_management(request):
    students = Student.objects.select_related("user").all()
    return render(request, "course_management/user_list.html", {"students": students})


@user_passes_test(is_admin)
def add_user(request):
    if request.method == "POST":
        user_form = CustomUserForm(request.POST, prefix="user")
        student_form = StudentForm(request.POST, prefix="student")

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, "کاربر با موفقیت اضافه شد.")
            return redirect("user_management")
    else:
        user_form = CustomUserForm(prefix="user")
        student_form = StudentForm(prefix="student")

    return render(
        request,
        "course_management/add_user.html",
        {"user_form": user_form, "student_form": student_form},
    )


@user_passes_test(is_admin)
def edit_user(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        user_form = CustomUserForm(request.POST, prefix="user", instance=student.user)
        student_form = StudentForm(request.POST, prefix="student", instance=student)

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            messages.success(request, "اطلاعات کاربر با موفقیت بروزرسانی شد.")
            return redirect("user_management")
    else:
        user_form = CustomUserForm(prefix="user", instance=student.user)
        student_form = StudentForm(prefix="student", instance=student)

    return render(
        request,
        "course_management/edit_user.html",
        {"user_form": user_form, "student_form": student_form, "student": student},
    )


@user_passes_test(is_admin)
def delete_user(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, "کاربر با موفقیت حذف شد.")
        return redirect("user_management")
    return render(request, "course_management/delete_user.html", {"student": student})


@user_passes_test(is_admin)
def add_course_classroom(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseClassroomForm(request.POST)
        if form.is_valid():
            course_classroom = form.save(commit=False)
            course_classroom.course = course
            course_classroom.save()
            messages.success(request, "کلاس با موفقیت به درس اضافه شد.")
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseClassroomForm()
    
    return render(
        request,
        'course_management/add_course_classroom.html',
        {'form': form, 'course': course}
    )

@user_passes_test(is_admin)
def delete_course_classroom(request, course_classroom_id):
    course_classroom = get_object_or_404(CourseClassroom, id=course_classroom_id)
    course_id = course_classroom.course.id
    if request.method == "POST":
        course_classroom.delete()
        messages.success(request, "کلاس با موفقیت از درس حذف شد.")
        return redirect('course_detail', course_id=course_id)
    
    return render(
        request,
        'course_management/delete_course_classroom.html',
        {'course_classroom': course_classroom}
    )

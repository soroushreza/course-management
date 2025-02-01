import json
from django.forms import ValidationError
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StudentProfileForm, CourseSelectionForm
from accounts.models import Student
from .models import Course, CourseClassroom, CourseSchedule, Enrollment, WeeklySchedule
from .services import EnrollmentService
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError


class Home(View):
    def get(self, request):
        return render(request, "course/home.html")


class StudentProfileView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            context = {
                "student": student,
                "readonly_fields": {
                    "شماره دانشجویی": student.student_number,
                    "ایمیل": student.email,
                    "کد ملی": student.national_id,
                    "سال ورود": student.admission_year,
                },
            }
            return render(request, "course/profile.html", context)
        except Student.DoesNotExist:
            messages.error(request, "پروفایل دانشجویی یافت نشد")
            return redirect("home")


class StudentProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            form = StudentProfileForm(instance=student)
            return render(request, "course/profile_edit.html", {"form": form})
        except Student.DoesNotExist:
            messages.error(request, "پروفایل دانشجویی یافت نشد")
            return redirect("home")

    def post(self, request):
        try:
            student = Student.objects.get(user=request.user)
            form = StudentProfileForm(request.POST, instance=student)

            if form.is_valid():
                form.save()
                messages.success(request, "اطلاعات با موفقیت به‌روزرسانی شد")
                return redirect("student_profile")

            return render(request, "course/profile_edit.html", {"form": form})

        except Student.DoesNotExist:
            messages.error(request, "پروفایل دانشجویی یافت نشد")
            return redirect("home")

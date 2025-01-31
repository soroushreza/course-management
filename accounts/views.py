from .models import CustomUser as User
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from accounts.forms import (
    PasswordResetForm,
    PasswordResetVerifyForm,
    StudentLoginForm,
    StudentRegistrationForm,
)
from accounts.models import Student
from django.contrib.auth.mixins import LoginRequiredMixin



class StudentRegistrationView(View):
    template_name = "accounts/register.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("student_profile")
        form = StudentRegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Create CustomUser instance
            user = User.objects.create_user(
                student_number=form.cleaned_data["student_number"],
                password=form.cleaned_data["password"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            # Create Student profile
            student = Student.objects.create(
                user=user,
                email=form.cleaned_data["email"],
                student_number=form.cleaned_data["student_number"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                major=form.cleaned_data["major"],
                national_id=form.cleaned_data["national_id"],
                admission_year=form.cleaned_data["admission_year"],
            )

            messages.success(
                request, "ثبت نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید."
            )
            return redirect("login")
        return render(request, self.template_name, {"form": form})


class StudentLoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("student_profile")
        form = StudentLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            next_url = request.GET.get("next", "student_profile")
            return redirect(next_url)
        return render(request, self.template_name, {"form": form})
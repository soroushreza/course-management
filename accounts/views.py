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


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "با موفقییت خارج شدید!!")
            return redirect("login")


class PasswordResetView(View):
    def get(self, request):
        # اگر کاربر قبلاً احراز هویت شده، فرم تغییر رمز را نشان بده
        if "reset_verified_user_id" in request.session:
            form = PasswordResetForm()
            return render(request, "accounts/password_reset_new.html", {"form": form})
        # در غیر این صورت فرم تأیید هویت را نشان بده
        form = PasswordResetVerifyForm()
        return render(request, "accounts/password_reset_verify.html", {"form": form})

    def post(self, request):
        # اگر کاربر قبلاً احراز هویت شده، رمز جدید را ثبت کن
        if "reset_verified_user_id" in request.session:
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                user = User.objects.get(id=request.session["reset_verified_user_id"])
                user.set_password(form.cleaned_data["new_password"])
                user.save()
                # پاک کردن اطلاعات نشست
                del request.session["reset_verified_user_id"]
                messages.success(request, "رمز عبور با موفقیت تغییر کرد")
                return redirect("login")
            return render(request, "accounts/password_reset_new.html", {"form": form})
        # در غیر این صورت اطلاعات کاربر را تأیید کن
        form = PasswordResetVerifyForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            request.session["reset_verified_user_id"] = user.id
            # نمایش فرم تغییر رمز
            return redirect("password_reset")
        return render(request, "accounts/password_reset_verify.html", {"form": form})

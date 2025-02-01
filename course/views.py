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


@login_required
def course_selection_view(request):
    form = CourseSelectionForm()
    return render(request, "course/course_selection.html", {"form": form})


@login_required
def get_department_courses(request):
    department_id = request.GET.get("department_id")
    if department_id:
        courses = (
            Course.objects.filter(department_id=department_id, capacity__gt=0)
            .prefetch_related("schedules")
            .values(
                "id",
                "name",
                "code",
                "credits",
                "instructor__first_name",
                "instructor__last_name",
                "capacity",
                "initial_capacity",
                "exam_date",
            )
        )

        # افزودن روز و زمان ارائه هر درس
        courses_data = []
        for course in courses:
            schedules = CourseSchedule.objects.filter(course_id=course["id"]).values(
                "day_of_week", "start_time", "end_time"
            )
            schedules_list = [
                {
                    "day": dict(CourseSchedule.DAYS_OF_WEEK)[s["day_of_week"]],
                    "start_time": s["start_time"].strftime("%H:%M"),
                    "end_time": s["end_time"].strftime("%H:%M"),
                }
                for s in schedules
            ]

            courses_data.append(
                {
                    **course,
                    "schedules": schedules_list,
                    "exam_date": (
                        course["exam_date"].strftime("%Y-%m-%d")
                        if course["exam_date"]
                        else "نامشخص"
                    ),
                }
            )

        return JsonResponse({"courses": courses_data})
    return JsonResponse({"courses": []})


@login_required
@require_POST
def enroll_course(request):
    course_id = request.POST.get("course_id")
    try:
        course = Course.objects.get(id=course_id)
        student = Student.objects.get(user=request.user)

        # استفاده از سرویس برای ثبت‌نام
        EnrollmentService.enroll_student(student, course)

        messages.success(request, f"درس {course.name} با موفقیت اضافه شد.")
        return JsonResponse(
            {"status": "success", "message": f"درس {course.name} با موفقیت اضافه شد."}
        )

    except Course.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "درس مورد نظر یافت نشد."}, status=404
        )
    except ValidationError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@login_required
@require_POST
def drop_course(request):
    course_id = request.POST.get("course_id")
    try:
        course = Course.objects.get(id=course_id)
        student = Student.objects.get(user=request.user)
        enrollment = Enrollment.objects.get(student=student, course=course)

        # افزایش ظرفیت درس
        course.capacity += 1
        course.save()

        # حذف از برنامه هفتگی
        WeeklySchedule.objects.filter(student=student, course=course).delete()

        # حذف ثبت‌نام
        enrollment.delete()

        return JsonResponse(
            {"status": "success", "message": f"درس {course.name} با موفقیت حذف شد."}
        )

    except (Course.DoesNotExist, Enrollment.DoesNotExist):
        return JsonResponse(
            {"status": "error", "message": "درس مورد نظر یافت نشد."}, status=404
        )


@login_required
def get_enrolled_courses(request):
    try:
        student = Student.objects.get(user=request.user)
        enrolled_courses = Enrollment.objects.filter(
            student=student, status="approved"
        ).select_related("course", "course__instructor")

        total_units = EnrollmentService.calculate_total_units(student)

        courses_data = [
            {
                "id": enrollment.course.id,
                "name": enrollment.course.name,
                "code": enrollment.course.code,
                "credits": enrollment.course.credits,
                "instructor": f"{enrollment.course.instructor.first_name} {enrollment.course.instructor.last_name}",
            }
            for enrollment in enrolled_courses
        ]

        return JsonResponse(
            {
                "status": "success",
                "courses": courses_data,
                "total_units": total_units,
                "max_units": student.max_units,
            }
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@login_required
def weekly_schedule_view(request):
    try:
        student = Student.objects.get(user=request.user)
        schedules = (
            WeeklySchedule.objects.filter(student=student)
            .select_related("course", "course__instructor")
            .order_by("day_of_week", "start_time")
        )

        # ساخت بازه‌های زمانی بر اساس کلاس‌ها
        unique_time_slots = sorted(
            set(
                (
                    schedule.start_time.strftime("%H:%M"),
                    schedule.end_time.strftime("%H:%M"),
                )
                for schedule in schedules
            )
        )

        schedules_data = []
        for schedule in schedules:
            if CourseClassroom.objects.filter(course=schedule.course).exists():
                schedules_data.append(
                    {
                        "day_of_week": schedule.day_of_week,
                        "start_time": schedule.start_time.strftime("%H:%M"),
                        "end_time": schedule.end_time.strftime("%H:%M"),
                        "course": {
                            "name": schedule.course.name,
                            "code": schedule.course.code,
                            "instructor": f"{schedule.course.instructor.first_name} {schedule.course.instructor.last_name}",
                            "classroom": (
                                CourseClassroom.objects.get(
                                    course=schedule.course
                                ).classroom.name
                                if schedule.course
                                else ""
                            ),
                            "exam_date": (
                                schedule.course.exam_date.strftime("%Y-%m-%d")
                                if schedule.course.exam_date
                                else "نامشخص"
                            ),
                        },
                    }
                )
            else:
                raise ValidationError('جزییات مربوط به کلاس درس هر درس را پر کنید!!')

        context = {
            "schedules": json.dumps(schedules_data, ensure_ascii=False),
            "time_slots": [f"{start} - {end}" for start, end in unique_time_slots],
            "days": WeeklySchedule.DAYS_OF_WEEK,
        }
        return render(request, "course/weekly_schedule.html", context)
    except Student.DoesNotExist:
        messages.error(request, "پروفایل دانشجویی یافت نشد")
        return redirect("home")

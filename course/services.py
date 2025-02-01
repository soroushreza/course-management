from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.aggregates import Sum
from course.models import CourseSchedule, Enrollment, WeeklySchedule



class EnrollmentService:
    @staticmethod
    def calculate_total_units(student):
        """محاسبه تعداد واحدهای انتخابی دانشجو"""
        return Enrollment.objects.filter(
            student=student, 
            status='approved'
        ).aggregate(total_units=Sum('course__credits'))['total_units'] or 0
    
    @staticmethod
    def get_student_courses(student, status=None):
        """دریافت دروس دانشجو با فیلتر وضعیت"""
        queryset = Enrollment.objects.filter(student=student)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    @staticmethod
    def validate_max_units(student, course):
        """بررسی تعداد واحدهای مجاز"""
        current_units = EnrollmentService.calculate_total_units(student)
        if current_units + course.credits > student.max_units:
            raise ValidationError(
                f'تعداد واحدهای انتخابی ({current_units + course.credits}) '
                f'از سقف مجاز ({student.max_units}) بیشتر است'
            )

    @staticmethod
    def validate_course_conflicts(student, course):
        # بررسی تداخل زمانی کلاس‌ها
        student_courses = Enrollment.objects.filter(
            student=student.id, status="approved"
        ).select_related("course")

        new_course_schedules = CourseSchedule.objects.filter(course=course)

        for new_schedule in new_course_schedules:
            existing_schedules = CourseSchedule.objects.filter(
                course__enrollment__student=student,
                course__enrollment__status="approved",
                day_of_week=new_schedule.day_of_week,
            )

            for existing_schedule in existing_schedules:
                if (
                    new_schedule.start_time <= existing_schedule.end_time
                    and new_schedule.end_time >= existing_schedule.start_time
                ):
                    raise ValidationError(
                        f"تداخل زمانی با درس {existing_schedule.course.name}"
                    )

        # بررسی تداخل زمان امتحان
        for enrolled_course in student_courses:
            if course.exam_date == enrolled_course.course.exam_date and (
                (
                    course.exam_start_time <= enrolled_course.course.exam_end_time
                    and course.exam_end_time >= enrolled_course.course.exam_start_time
                )
            ):
                raise ValidationError(
                    f"تداخل زمان امتحان با درس {enrolled_course.course.name}"
                )

    @staticmethod
    def check_prerequisites(student, course):
        prerequisites = course.prerequisites.all()
        if prerequisites.exists():
            for prereq in prerequisites:
                if not Enrollment.objects.filter(
                    student=student.id, course=prereq.required_course, status="approved"
                ).exists():
                    raise ValidationError(
                        f'این درس --{prereq.required_course.name}-- که پیش نیاز هست را نگذرانده اید!!'
                    )

    @staticmethod
    def validate_corequisites(student, course):
        """
        بررسی همنیازها - درس همنیاز یا باید قبلا پاس شده باشد یا در این ترم برداشته شود
        """
        corequisites = course.get_all_corequisites()
        if corequisites:
            for coreq in corequisites:
                # بررسی اینکه آیا درس همنیاز قبلاً پاس شده
                previously_passed = Enrollment.objects.filter(
                    student=student.id,
                    course=coreq,
                    status='approved'
                ).exists()
                
                # بررسی اینکه آیا درس همنیاز در این ترم انتخاب شده
                current_term_enrollment = Enrollment.objects.filter(
                    student=student.id,
                    course=coreq,
                    status='pending',
                    enrollment_date__year=datetime.now().year,
                    enrollment_date__month__in=[
                        # ماه‌های ترم جاری
                        datetime.now().month,
                        datetime.now().month + 1,
                        datetime.now().month + 2,
                        datetime.now().month + 3
                    ]
                ).exists()
                
                if not (previously_passed or current_term_enrollment):
                    raise ValidationError(
                        f'درس {coreq.name} همنیاز است و باید همزمان یا قبلاً گذرانده شود'
                    )

    @staticmethod
    @transaction.atomic
    def enroll_student(student, course):
        # بررسی ظرفیت
        if course.capacity <= 0:
            raise ValidationError("ظرفیت درس تکمیل شده است")
        
        # بررسی تعداد واحدها
        EnrollmentService.validate_max_units(student, course)

        # بررسی تداخل‌ها
        EnrollmentService.validate_course_conflicts(student, course)

        # بررسی پیش‌نیازها
        EnrollmentService.check_prerequisites(student, course)

        # ثبت‌نام
        enrollment = Enrollment.objects.create(
            student=student, course=course, status="approved"
        )

        # به‌روزرسانی ظرفیت
        course.capacity -= 1
        course.save()

        # ایجاد برنامه هفتگی
        for schedule in course.schedules.all():
            WeeklySchedule.objects.create(
                student=student,
                course=course,
                day_of_week=schedule.day_of_week,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
            )

        return enrollment

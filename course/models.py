from django.db import models
from accounts.models import CustomUser as User
from accounts.models import Student


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    credits = models.IntegerField()
    capacity = models.IntegerField()
    initial_capacity = models.IntegerField()
    exam_date = models.DateField()
    exam_start_time = models.TimeField()
    exam_end_time = models.TimeField()
    department = models.ForeignKey("Department", on_delete=models.PROTECT)
    instructor = models.ForeignKey("Instructor", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "درس ها"

    def get_all_corequisites(self):
        """Returns all corequisite courses"""
        return Course.objects.filter(is_corequisite_for__course=self)


class Department(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "نام دانشکده"
        verbose_name_plural = "نام دانشکده ها"

    def __str__(self):
        return self.name


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    class Meta:
        verbose_name = "مدرس"
        verbose_name_plural = "مدرس ها"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس ها"

    def __str__(self):
        return self.name


class CourseClassroom(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_classroom"
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "کلاس درس"
        verbose_name_plural = "کلاس درس ها"

    def __str__(self):
        return f"{self.course.name} = {self.classroom.name}"


class Prerequisite(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="prerequisites"
    )
    required_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="is_prerequisite_for"
    )
    
    def __str__(self):
        return f"{self.course.name} perquisite"

    class Meta:
        verbose_name = "پیش نیاز"
        verbose_name_plural = "پیش نیاز ها"
        unique_together = ["course", "required_course"]


class Corequisite(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="corequisites"
    )
    required_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="is_corequisite_for"
    )

    def __str__(self):
        return f"{self.course.name} corequisite"
    class Meta:
        verbose_name = "هم نیاز"
        verbose_name_plural = "هم نیاز ها ها"
        unique_together = ["course", "required_course"]


class CourseSchedule(models.Model):
    DAYS_OF_WEEK = [
        (1, "شنبه"),
        (2, "یکشنبه"),
        (3, "دوشنبه"),
        (4, "سه‌شنبه"),
        (5, "چهارشنبه"),
        (6, "پنج‌شنبه"),
        (7, "جمعه"),
    ]

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="schedules"
    )
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.ForeignKey("Classroom", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.course.name} {self.day_of_week}"

    class Meta:
        verbose_name = "مشخصات درس"
        verbose_name_plural = "مشخصات درس ها"
        unique_together = ["course", "day_of_week", "start_time"]


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    
    def __str__(self):
        return f"{self.student.first_name} {self.enrollment_date} {self.status}"

    class Meta:
        verbose_name = " انتخاب واحد"
        verbose_name_plural = "  انتخاب واحد درس ها"
        unique_together = ["student", "course"]


class WeeklySchedule(models.Model):
    DAYS_OF_WEEK = [
        (1, "شنبه"),
        (2, "یکشنبه"),
        (3, "دوشنبه"),
        (4, "سه‌شنبه"),
        (5, "چهارشنبه"),
        (6, "پنج‌شنبه"),
        (7, "جمعه"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.student.first_name} {self.day_of_week}"

    class Meta:
        verbose_name = "برنامه هفتگی"
        verbose_name_plural = "برنامه های هفتگی "
        unique_together = ["student", "course", "day_of_week"]

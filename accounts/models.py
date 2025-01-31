from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, student_number, password=None, **extra_fields):
        if not student_number:
            raise ValueError("شماره دانشجویی الزامی است")
        user = self.model(student_number=student_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(student_number, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField()
    student_number = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = "student_number"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"


class UserLevel(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "سطح کاربر "
        verbose_name_plural = "سطح های کاربر "

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="student_profile"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    national_id = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    major = models.CharField(max_length=100)
    year = models.DateField(auto_now_add=True)
    max_units = models.IntegerField(default=20)
    student_number = models.CharField(max_length=9, unique=True)
    admission_year = models.IntegerField()

    def __str__(self):
        return f"{self.student_number} - {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "دانشجو"
        verbose_name_plural = "دانشجو ها"

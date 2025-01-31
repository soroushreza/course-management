from django.contrib import admin
from .models import CustomUser, UserLevel, Student

# Register your models here.



@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('student_number', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('student_number', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')


@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_number', 'first_name', 'last_name', 'email', 'national_id', 'phone_number', 'major', 'year', 'max_units', 'admission_year')
    search_fields = ('student_number', 'first_name', 'last_name', 'email', 'national_id')
    list_filter = ('year', 'admission_year', 'major')
    readonly_fields = ('user',)

from django.contrib import admin
from .models import CourseClassroom, Course, Department, Instructor, Classroom, Prerequisite, Corequisite, CourseSchedule, Enrollment, WeeklySchedule

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credits', 'capacity', 'initial_capacity', 'exam_date', 'exam_start_time', 'exam_end_time', 'department', 'instructor')
    search_fields = ('name', 'code')
    list_filter = ('department', 'instructor')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('department',)

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'department')
    search_fields = ('name',)
    list_filter = ('department',)

@admin.register(Prerequisite)
class PrerequisiteAdmin(admin.ModelAdmin):
    list_display = ('course', 'required_course')

@admin.register(Corequisite)
class CorequisiteAdmin(admin.ModelAdmin):
    list_display = ('course', 'required_course')

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'get_day_of_week_display', 'start_time', 'end_time', 'classroom')
    list_filter = ('day_of_week', 'classroom')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'status')
    list_filter = ('status', 'enrollment_date')
    date_hierarchy = 'enrollment_date'

@admin.register(WeeklySchedule)
class WeeklyScheduleAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'get_day_of_week_display', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'student')


@admin.register(CourseClassroom)
class CourseClassroomAdmin(admin.ModelAdmin):
    list_display = ('course',)

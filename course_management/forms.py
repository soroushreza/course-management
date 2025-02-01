# forms.py
from django import forms
from accounts.models import CustomUser, Student
from course.models import Course, CourseClassroom, CourseSchedule, Prerequisite, Corequisite



class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['student_number', 'email', 'is_active', 'is_staff', 'is_superuser']
        labels = {
            'student_number': 'شماره دانشجویی',
            'email': 'ایمیل',
            'is_active': 'فعال',
            'is_staff': ';''کارمند',
            'is_superuser': 'ادمین',
        }
        help_texts = {
            'is_active': '',
            'is_staff': '',
            'is_superuser': '',
        }
        widgets = {
            'student_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'national_id', 
                    'phone_number', 'major', 'max_units', 'student_number', 
                    'admission_year']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'national_id': 'کد ملی',
            'phone_number': 'شماره تلفن',
            'major': 'رشته تحصیلی',
            'max_units': 'حداکثر واحد مجاز',
            'student_number': 'شماره دانشجویی',
            'admission_year': 'سال ورود',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'max_units': forms.NumberInput(attrs={'class': 'form-control'}),
            'student_number': forms.TextInput(attrs={'class': 'form-control'}),
            'admission_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'credits', 'capacity', 'initial_capacity', 'exam_date', 'exam_start_time', 'exam_end_time', 'department', 'instructor']
        labels = {
            'name': 'نام درس',
            'code': 'کد درس',
            'credits': 'تعداد واحد',
            'capacity': 'ظرفیت',
            'initial_capacity': 'ظرفیت اولیه',
            'exam_date': 'تاریخ امتحان',
            'exam_start_time': 'زمان شروع امتحان',
            'exam_end_time': 'زمان پایان امتحان',
            'department': 'دانشکده',
            'instructor': 'استاد',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'exam_start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'exam_end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'instructor': forms.Select(attrs={'class': 'form-control'}),
        }

class CourseScheduleForm(forms.ModelForm):
    class Meta:
        model = CourseSchedule
        fields = ['day_of_week', 'start_time', 'end_time', 'classroom']
        labels = {
            'day_of_week': 'روز هفته',
            'start_time': 'زمان شروع',
            'end_time': 'زمان پایان',
            'classroom': 'کلاس',
        }
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'classroom': forms.Select(attrs={'class': 'form-control'}),
        }

class PrerequisiteForm(forms.ModelForm):
    class Meta:
        model = Prerequisite
        fields = ['required_course']
        labels = {
            'required_course': 'پیش‌نیاز',
        }
        widgets = {
            'required_course': forms.Select(attrs={'class': 'form-control'}),
        }

class CorequisiteForm(forms.ModelForm):
    class Meta:
        model = Corequisite
        fields = [ 'required_course']
        labels = {
            'required_course': 'هم‌نیاز',
        }
        widgets = {
            'required_course': forms.Select(attrs={'class': 'form-control'}),
        }
    

class CourseClassroomForm(forms.ModelForm):
    class Meta:
        model = CourseClassroom
        fields = ['classroom']
        labels = {
            'classroom': 'کلاس',
        }
        widgets = {
            'classroom': forms.Select(attrs={'class': 'form-control'}),
        }

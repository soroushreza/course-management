from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser as User
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = [
            'student_number', 'first_name', 'last_name', 'major',
            'email', 'national_id', 'admission_year'
        ]
        labels = {
            'student_number': 'شماره دانشجویی',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'major': 'رشته تحصیلی',
            'email': 'ایمیل',
            'national_id': 'شماره ملی',
            'admission_year': 'سال ورود',
        }
        widgets = {
            'student_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'admission_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_student_number(self):
        student_number = self.cleaned_data.get("student_number")
        if User.objects.filter(student_number=student_number).exists():
            raise forms.ValidationError("این شماره دانشجویی قبلاً ثبت شده است")
        elif not student_number:
            raise forms.ValidationError("شماره دانشجویی نمی تواند خالی باشد.")
        elif not str(student_number).isdigit() or len(str(student_number)) != 9:
            raise forms.ValidationError(
                "شماره دانشجویی باید 9 رقم باشد و تنها شامل اعداد باشد."
            )
        return student_number

    def clean_national_id(self):
        national_id = self.cleaned_data.get("national_id")
        if Student.objects.filter(national_id=national_id).exists():
            raise forms.ValidationError("این شماره ملی قبلاً ثبت شده است")
        elif not national_id:
            raise forms.ValidationError("شماره ملی نمی تواند خالی باشد.")
        elif not str(national_id).isdigit():
            raise forms.ValidationError("شماره ملی باید تنها شامل اعداد باشد.")
        elif len(str(national_id)) != 10:
            raise forms.ValidationError("شماره ملی باید 10 رقم باشد.")
        return national_id

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت شده است")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("رمز عبور و تکرار آن باید یکسان باشند")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class StudentLoginForm(forms.Form):
    student_number = forms.CharField(label="شماره دانشجویی")
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        student_number = cleaned_data.get("student_number")
        password = cleaned_data.get("password")

        if student_number and password:
            user = authenticate(student_number=student_number, password=password)
            if not user:
                raise forms.ValidationError("شماره دانشجویی یا رمز عبور اشتباه است")
            cleaned_data["user"] = user
        return cleaned_data

    def clean_student_number(self):
        student_number = self.cleaned_data.get("student_number")
        if not student_number:
            raise forms.ValidationError("شماره دانشجویی نمی تواند خالی باشد.")
        elif not str(student_number).isdigit() or len(str(student_number)) != 9:
            raise forms.ValidationError(
                "شماره دانشجویی باید 9 رقم باشد و تنها شامل اعداد باشد."
            )
        return student_number


class PasswordResetVerifyForm(forms.Form):
    student_number = forms.CharField(
        label="شماره دانشجویی", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="ایمیل", widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    def clean(self):
        cleaned_data = super().clean()
        student_number = cleaned_data.get("student_number")
        email = cleaned_data.get("email")

        if student_number and email:
            user = User.objects.filter(
                student_number=student_number, email=email
            ).first()

            if not user:
                raise forms.ValidationError("اطلاعات وارد شده صحیح نمی‌باشد")

            cleaned_data["user"] = user
        return cleaned_data

    def clean_student_number(self):
        student_number = self.cleaned_data.get("student_number")
        if not student_number:
            raise forms.ValidationError("شماره دانشجویی نمی تواند خالی باشد.")
        elif not str(student_number).isdigit() or len(str(student_number)) != 9:
            raise forms.ValidationError(
                "شماره دانشجویی باید 9 رقم باشد و تنها شامل اعداد باشد."
            )
        return student_number


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    confirm_password = forms.CharField(
        label="تکرار رمز عبور جدید",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("رمز عبور و تکرار آن باید یکسان باشند")
        return cleaned_data

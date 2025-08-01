from django import forms
from .models import Applicant, Interviewer, Department
from django.core.exceptions import ValidationError
import datetime


class ApplicationForm(forms.ModelForm):
    """新生申请表单"""

    class Meta:
        model = Applicant
        fields = [
            'name', 'grade', 'student_id', 'major', 'email', 'phone',
            'first_choice', 'second_choice', 'resume'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'first_choice': forms.Select(attrs={'class': 'form-control'}),
            'second_choice': forms.Select(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_student_id(self):
        """验证学号格式"""
        student_id = self.cleaned_data.get('student_id')
        if not student_id.isdigit():
            raise ValidationError("学号必须为数字")
        return student_id

    def clean_phone(self):
        """验证手机号格式"""
        phone = self.cleaned_data.get('phone')
        if not (phone.isdigit() and len(phone) == 11):
            raise ValidationError("请输入有效的11位手机号码")
        return phone

    def clean(self):
        """验证志愿部门不能相同"""
        cleaned_data = super().clean()
        first_choice = cleaned_data.get('first_choice')
        second_choice = cleaned_data.get('second_choice')

        if first_choice and second_choice and first_choice == second_choice:
            raise ValidationError("第一志愿和第二志愿不能选择同一个部门")

        return cleaned_data

    def clean_resume(self):
        """验证简历文件格式"""
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.endswith('.pdf'):
                raise ValidationError("简历必须是PDF格式")
            # 限制文件大小（5MB）
            if resume.size > 5 * 1024 * 1024:
                raise ValidationError("简历文件大小不能超过5MB")
        return resume


class InterviewerLoginForm(forms.Form):
    """面试官登录表单"""
    student_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入学号'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'})
    )


class DepartmentForm(forms.ModelForm):
    """部门表单"""

    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class InterviewerForm(forms.ModelForm):
    """面试官表单"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Interviewer
        fields = ['name', 'student_id', 'department_team', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department_team': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """验证密码一致性"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("两次输入的密码不一致")

        return cleaned_data

    def save(self, commit=True):
        """保存时加密密码"""
        interviewer = super().save(commit=False)
        interviewer.set_password(self.cleaned_data['password'])
        if commit:
            interviewer.save()
        return interviewer

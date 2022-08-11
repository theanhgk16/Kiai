
from django import forms
from matplotlib import widgets
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'name', 'phone',)


# class MyUserChangeForm(UserChangeForm):

#     class Meta:
#         model = User
#         # fields = ('username', 'fullname', 'phone')
#         fields = '__all__'
#         widgets = {
#             'code': forms.TextInput(attrs={'readonly': True}),
#             'name': forms.TextInput(attrs={'type': 'text'}),
#             'birthday': forms.DateInput(attrs={'type': 'date'}),
#             'sex': forms.Select(attrs={'class': 'form-select'}),
#             'phone': forms.TextInput(attrs={'type': 'number'}),
#             'address': forms.TextInput(attrs={'type': 'text'}),
#             'cmnd': forms.TextInput(attrs={'type': 'number'}),
#         }
class MyUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'name', 'phone', 'address')


# class StudentForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = '__all__'
#         widgets = {
#             'code': forms.TextInput(attrs={'readonly': True}),
#             'code': forms.TextInput(attrs={'type': 'text'}),
#             'name': forms.TextInput(attrs={'type': 'text'}),
#             'birthday': forms.DateInput(attrs={'type': 'date'}),
#             'sex': forms.Select(attrs={'class': 'form-select'}),
#             'phone': forms.TextInput(attrs={'type': 'number'}),
#             'address': forms.TextInput(attrs={'type': 'text'}),
#             'cmnd': forms.TextInput(attrs={'type': 'number'}),
#         }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'type': 'text'}),
        }


class ClassesForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = '__all__'


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'})
        }


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'


class EnrollmentForm(forms.ModelForm):

    class Meta:
        model = Enrollment
        fields = '__all__'
        widgets = {
            'note': forms.Textarea(attrs={'type': 'text'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ['doc']
        widgets = {
                'doc': forms.FileField(label='Chọn một file'),
            }
# class DocumentForm(forms.Form):
#     class Meta:
#         model = FileModel
#         fields = '__all__'
#         widgets = {
#                 'doc': forms.FileField(label='Chọn một file'),
#             }
        
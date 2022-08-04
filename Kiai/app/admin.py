# from django.contrib import admin
from .models import *

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import forms, models


class MyUserAdmin(UserAdmin):
    add_form = forms.MyUserCreationForm
    form = forms.MyUserChangeForm
    model = models.User
    list_display = ['username', 'name', 'phone', 'address']


admin.site.register(models.User, MyUserAdmin)
admin.site.register(Subject)
admin.site.register(Classes)
admin.site.register(Exam)
admin.site.register(Result)
admin.site.register(Enrollment)
admin.site.register(ExamManagement)
admin.site.register(Question)
admin.site.register(Answer)

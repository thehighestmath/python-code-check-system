from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Student, Teacher


class TeacherAdmin(ModelAdmin):
    model = Teacher


class StudentAdmin(ModelAdmin):
    model = Student


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_student', 'is_teacher'
    )


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)

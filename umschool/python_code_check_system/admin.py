from django.contrib import admin

from .models import Solution, Student, Task, Test

admin.site.register(Student)
admin.site.register(Solution)
admin.site.register(Task)
admin.site.register(Test)

from django.contrib import admin

from .models import Student, Solution, Task, Tests


admin.site.register(Student)
admin.site.register(Solution)
admin.site.register(Task)
admin.site.register(Tests)


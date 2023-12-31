from django.http import HttpResponse
from django.shortcuts import render
from .models import Task, Student
from django.views.generic import ListView


class TaskHome(ListView):
    model = Task
    template_name = 'python_code_check_system/tasks.html'
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['main'] = 'Задания'
        context['title'] = 'Задания'
        return context


class StudentHome(ListView):
    model = Student
    template_name = 'python_code_check_system/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['main'] = 'Профиль'
        context['title'] = 'Профиль'
        return context


def add_to_db_page(request):
    return render(request, 'python_code_check_system/add_to_db_page.html')

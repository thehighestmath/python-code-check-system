from django.shortcuts import render, redirect
from .models import Task, Student
from django.views.generic import ListView, CreateView
from .forms import TaskForm
from django.views.generic import TemplateView


class TaskHome(ListView):
    model = Task
    template_name = 'python_code_check_system/tasks.html'
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskHome, self).get_context_data(**kwargs)
        context['main'] = 'Задания'
        context['title'] = 'Задания'
        return context

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(request, 'python_code_check_system/tasks.html', {'tasks' : tasks})


class StudentHome(ListView):
    model = Student
    template_name = 'python_code_check_system/profile.html'
    context_object_name = 'profile'

    def get_queryset(self):
        return Student.objects.get(pk=1)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['main'] = 'Профиль'
        context['title'] = 'Профиль'
        return context

    def get(self, request, *args, **kwargs):
        return render(request, 'python_code_check_system/profile.html')


class AddTask(CreateView):
    model = Task
    form = TaskForm()
    fields = ['name', 'complexity', 'description']
    template_name = 'python_code_check_system/add_to_db_page.html'
    extra_context = {
        'form': form
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['main'] = 'Задания'
        context['title'] = 'Задания'
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            tasks = Task.objects.all()
            return render(request, 'python_code_check_system/tasks.html', {'tasks': tasks})


class Home(TemplateView):
    template_name = 'python_code_check_system/index.html'


class Contacts(TemplateView):
    template_name = 'python_code_check_system/contacts.html'


class About(TemplateView):
    template_name = 'python_code_check_system/about.html'


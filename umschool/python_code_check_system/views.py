from django.http import HttpResponse
from django.shortcuts import render
from .models import Task


def home(request):
    return render(request, 'python_code_check_system/index.html')


def profile(request):
    return render(request, 'python_code_check_system/profile.html')


def tasks(request):
    ctx = Task.objects.all()
    return render(request, 'python_code_check_system/tasks.html', {'ctx' : ctx})


def about(request):
    return render(request, 'python_code_check_system/about.html')


def contacts(request):
    return render(request, 'python_code_check_system/contacts.html')


def profile(request):
    return render(request, 'python_code_check_system/profile.html')

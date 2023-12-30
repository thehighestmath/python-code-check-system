from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'python_code_check_system/index.html')


def authorization_page(request):
    pass


def profile(request):
    pass


def tasks(request):
    return render(request, 'python_code_check_system/tasks.html')

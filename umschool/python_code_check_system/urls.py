from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import TaskHome, StudentHome, AddTask, Home, Contacts, About

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('tasks/', TaskHome.as_view(), name='tasks'),
    path('about/', About.as_view(), name='about'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('profile/', StudentHome.as_view(), name='profile'),
    path('tasks/add_tasks/', AddTask.as_view(), name='add_to_db_page')
]

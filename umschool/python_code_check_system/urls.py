from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import TemplateView
from  .views import TaskHome, StudentHome

urlpatterns = [
    path('', TemplateView.as_view(template_name='python_code_check_system/index.html'), name='home'),
    path('tasks/', TaskHome.as_view(), name='tasks'),
    path('about/', TemplateView.as_view(template_name='python_code_check_system/about.html'), name='about'),
    path('contacts/', TemplateView.as_view(template_name='python_code_check_system/contacts.html'), name='contacts'),
    path('profile/', StudentHome.as_view(), name='profile'),
    path('tasks/tasks/', views.add_to_db_page, name='add_to_db_page')
]

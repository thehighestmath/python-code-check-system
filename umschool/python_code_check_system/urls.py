from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import TaskHomeListView, StudentHomeListView, AddTask, HomeTemplateView, ContactsTemplateView, AboutTemplateView, TaskDetailView

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('tasks/', TaskHomeListView.as_view(), name='tasks'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('profile/', StudentHomeListView.as_view(), name='profile'),
    path('tasks/add_tasks/', AddTask.as_view(), name='add_to_db_page'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]

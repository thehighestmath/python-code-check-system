from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_to_db_page, name='add_to_db_page'),
]

from django.urls import path

from .views import (
    AboutTemplateView,
    AddSolutionView,
    AddTask,
    ContactsTemplateView,
    HomeTemplateView,
    SolutionListView,
    StudentHomeListView,
    TaskDetailView,
    TaskHomeListView,
)

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("tasks/", TaskHomeListView.as_view(), name="tasks"),
    path("about/", AboutTemplateView.as_view(), name="about"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("profile/", StudentHomeListView.as_view(), name="profile"),
    path("tasks/add_tasks/", AddTask.as_view(), name="add_to_db_page"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("solutions/add/", AddSolutionView.as_view(), name="solutions-add"),
    path("solutions/", SolutionListView.as_view(), name="solutions"),
    path("solutions/", SolutionDetailView.as_view(), name="solutions"),
]

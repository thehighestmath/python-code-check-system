from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import SolutionForm, TaskForm
from .models import Solution, Student, Task
from .tasks import check_stundet_code_task, scheduled_task


class TaskHomeListView(ListView):
    model = Task
    template_name = 'python_code_check_system/tasks.html'
    context_object_name = 'all_tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskHomeListView, self).get_context_data(**kwargs)
        context['main'] = 'Задания'
        context['title'] = 'Задания'
        return context

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        import time

        scheduled_task.delay(int(time.time()))
        return render(
            request, 'python_code_check_system/tasks.html', {'all_tasks': tasks}
        )


class StudentHomeListView(ListView):
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
    success_url = 'tasks/'
    extra_context = {'form': form}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['main'] = 'Задания'
        context['title'] = 'Задания'
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tasks/', permanent=True)


class HomeTemplateView(TemplateView):
    template_name = 'python_code_check_system/index.html'


class ContactsTemplateView(TemplateView):
    template_name = 'python_code_check_system/contacts.html'


class AboutTemplateView(TemplateView):
    template_name = 'python_code_check_system/about.html'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'python_code_check_system/task_detail_view.html'
    context_object_name = 'task'


class AddSolutionView(CreateView):
    model = Solution
    form = SolutionForm()
    fields = ['student_id', 'source_code', 'task_id']
    success_url = 'solutions/'
    extra_context = {'form': form}

    def post(self, request, *args, **kwargs):
        form = SolutionForm(request.POST)
        if form.is_valid():
            instance = form.save()
            added_id = instance.id
            check_stundet_code_task.delay(added_id)
            return redirect('/solutions/', permanent=True)
        return HttpResponse("Ошибка: форма не валидна")


class SolutionListView(ListView):
    model = Solution
    context_object_name = 'solutions'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SolutionListView, self).get_context_data(**kwargs)
        context['main'] = 'Решения'
        context['title'] = 'Решения'
        return context

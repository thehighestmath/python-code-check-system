from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import SolutionForm, TaskForm, TestFormSet
from .models import Solution, Student, Task
from .tasks import check_stundet_code_task


class TaskHomeListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'python_code_check_system/tasks.html'
    context_object_name = 'all_tasks'
    login_url = '/accounts/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main'] = 'Задания'
        context['title'] = 'Задания'
        return context

    def get_queryset(self):
        """Показываем только активные задания."""
        return Task.objects.filter(is_active=True).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        return render(request, 'python_code_check_system/tasks.html', {'all_tasks': tasks})


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
    form_class = TaskForm
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['main'] = 'Задания'
        context['title'] = 'Задания'
        if self.request.POST:
            context['tests'] = TestFormSet(self.request.POST)
        else:
            context['tests'] = TestFormSet()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tests_form_set = self.get_context_data()['tests']
        if tests_form_set.is_valid():
            tests_form_set.instance = self.object
            tests_form_set.save()
        else:
            return HttpResponseBadRequest("Ошибка: неверные данные в формсете")
        return response


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


class AddSolutionView(LoginRequiredMixin, CreateView):
    model = Solution
    form_class = SolutionForm
    template_name = 'python_code_check_system/solution_form.html'
    success_url = '/solutions/'
    login_url = '/accounts/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        task_id = self.request.GET.get('task')
        if task_id:
            kwargs['task_id'] = task_id
        return kwargs

    def form_valid(self, form):
        # Автоматически устанавливаем студента
        if self.request.user.is_student:
            try:
                student = Student.objects.get(user=self.request.user)
                form.instance.student = student
            except Student.DoesNotExist:
                # Создаем студента если его нет
                student = Student.objects.create(user=self.request.user)
                form.instance.student = student

        response = super().form_valid(form)
        # Запускаем проверку кода только если не в тестовом окружении
        if not settings.TESTING:
            check_stundet_code_task.delay(self.object.id)
        return response


class SolutionListView(LoginRequiredMixin, ListView):
    model = Solution
    context_object_name = 'solutions'
    login_url = '/accounts/login/'

    def get_queryset(self):
        """Показываем только решения текущего пользователя."""
        if self.request.user.is_student:
            try:
                student = Student.objects.get(user=self.request.user)
                return Solution.objects.filter(student=student).order_by('-created_at')
            except Student.DoesNotExist:
                return Solution.objects.none()
        return Solution.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main'] = 'Решения'
        context['title'] = 'Решения'
        return context


class SolutionDetailView(DetailView):
    """Детальный просмотр решения."""

    model = Solution
    template_name = 'python_code_check_system/solution_detail.html'
    context_object_name = 'solution'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main'] = 'Решение'
        context['title'] = f"Решение для {self.object.task.name}"
        return context

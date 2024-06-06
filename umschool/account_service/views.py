from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.views.generic import TemplateView

from .forms import LoginForm, StudentSignUpForm, TeacherSignUpForm, StudentViewForm, TeacherViewForm, BaseViewForm
from .models import CustomUser, Student, Teacher


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = LoginForm
    template_name = 'account_service/login.html'


class ProfileView(View):
    def get(self, request, **kwargs):
        if request.user.is_student:
            student = Student.objects.get(user_id=request.user.id)
            base_form = BaseViewForm(instance=request.user)
            advanced_form = StudentViewForm(instance=student)

        elif request.user.is_teacher:
            teacher = Teacher.objects.get(user_id=request.user.id)
            base_form = BaseViewForm(instance=request.user)
            advanced_form = TeacherViewForm(instance=teacher)

        else:
            base_form = BaseViewForm(instance=request.user)
            advanced_form = None

        return render(request, 'account_service/profile.html', {
            'base_form': base_form,
            'advanced_form': advanced_form,
        })


class SignUpView(TemplateView):
    template_name = 'account_service/signup.html'


class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = 'account_service/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'студент'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')


class TeacherSignUpView(CreateView):
    model = CustomUser
    form_class = TeacherSignUpForm
    template_name = 'account_service/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'учитель'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')

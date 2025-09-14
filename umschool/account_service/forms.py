from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.db import transaction

from .models import CustomUser, Student, Teacher


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['username'].label = "Логин"
        self.fields['password'].label = "Пароль"
        submit = Submit('button', 'Войти')
        submit.field_classes = 'btn btn-outline-primary btn-lg btn-block'
        self.helper.add_input(submit)


class BaseViewForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
        )
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
        self.fields['username'].help_text = None
        self.fields.pop('password')


class StudentViewForm(UserChangeForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
        self.fields.pop('password')


class TeacherViewForm(UserChangeForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
        self.fields.pop('password')


class BaseSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Подтвердите пароль',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        for field_name in labels.keys():
            self.fields[field_name].help_text = None
            self.fields[field_name].label = labels[field_name]

        self.helper = FormHelper()

        submit = Submit('button', 'Зарегистрироваться')
        submit.field_classes = 'btn btn-outline-primary btn-lg btn-block'
        self.helper.add_input(submit)


class StudentSignUpForm(BaseSignUpForm):
    @transaction.atomic
    def save(self, commit=False):
        user = super().save(commit=commit)
        user.is_student = True
        user.save()
        Student.objects.create(user=user)
        return user


class TeacherSignUpForm(BaseSignUpForm):
    @transaction.atomic
    def save(self, commit=False):
        user = super().save(commit=commit)
        user.is_teacher = True
        user.save()
        Teacher.objects.create(user=user)
        return user

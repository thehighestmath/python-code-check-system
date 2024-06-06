from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm
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
    subscriber_count = forms.IntegerField(label='Количество подписчиков', min_value=0, required=False)
    tiktok_link = forms.URLField(label='Ссылка на tiktok', required=False)
    youtube_link = forms.URLField(label='Ссылка на youtube', required=False)

    field_order = ['first_name', 'last_name', 'subscriber_count', 'tiktok_link', 'youtube_link']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_blogger = True
        user.save()
        data = self.cleaned_data
        for key in ('first_name', 'last_name', 'username', 'password1', 'password2'):
            data.pop(key, None)
        data['subscriber_count'] = 0 if data['subscriber_count'] is None else data['subscriber_count']
        student = Student.objects.create(user=user, **data)
        return user


class TeacherSignUpForm(BaseSignUpForm):
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_musician = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user

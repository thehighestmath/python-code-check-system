from django.forms import ModelForm, Textarea, TextInput, ModelChoiceField, Select, CharField
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
import re

from .models import Solution, Task, Test

TestFormSet = inlineformset_factory(Task, Test, fields=('input_data', 'output_data'), extra=1, can_delete=True)


class TaskForm(ModelForm):
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Проверяем, что название не содержит только пробелы
            if not name.strip():
                raise ValidationError('Название не может состоять только из пробелов')

            # Проверяем, что название не начинается с цифры
            if name[0].isdigit():
                raise ValidationError('Название не может начинаться с цифры')

        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            # Проверяем, что описание не содержит только пробелы
            if not description.strip():
                raise ValidationError('Описание не может состоять только из пробелов')

        return description

    class Meta:
        model = Task
        fields = ['name', 'complexity', 'description']

        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите название задания',
                    'maxlength': '255',
                }
            ),
            'complexity': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'description': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Опишите задание подробно',
                    'rows': 5,
                    'maxlength': '5000',
                }
            ),
        }


class SolutionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        task_id = kwargs.pop('task_id', None)
        super().__init__(*args, **kwargs)
        if user and user.is_student:
            # Скрываем поле student, так как оно будет заполнено автоматически
            self.fields.pop('student', None)

        # Настраиваем поле task как выпадающий список
        self.fields['task'] = ModelChoiceField(
            queryset=Task.objects.filter(is_active=True).order_by('name'),
            empty_label="Выберите задание",
            widget=Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        )

        # Если передан task_id, устанавливаем его как начальное значение
        if task_id:
            try:
                task = Task.objects.get(id=task_id, is_active=True)
                self.fields['task'].initial = task
            except Task.DoesNotExist:
                pass

    def clean_source_code(self):
        source_code = self.cleaned_data.get('source_code')
        if source_code:
            # Проверяем, что код не пустой
            if not source_code.strip():
                raise ValidationError('Код не может быть пустым')

            # Проверяем минимальную длину
            if len(source_code.strip()) < 10:
                raise ValidationError('Код должен содержать минимум 10 символов')

            # Проверяем максимальную длину
            if len(source_code) > 10000:
                raise ValidationError('Код не должен превышать 10000 символов')

            # Проверяем, что код содержит хотя бы одну строку
            lines = source_code.strip().split('\n')
            if len(lines) < 1:
                raise ValidationError('Код должен содержать хотя бы одну строку')

        return source_code

    def clean(self):
        cleaned_data = super().clean()
        source_code = cleaned_data.get('source_code')
        task = cleaned_data.get('task')

        # Дополнительные проверки
        if source_code and task:
            # Проверяем, что студент не отправляет одинаковый код для одного задания
            user = getattr(self, 'user', None)
            if user and hasattr(user, 'is_student') and user.is_student:
                from .models import Student

                try:
                    student = Student.objects.get(user=user)
                    existing_solutions = Solution.objects.filter(student=student, task=task, source_code=source_code)
                    if existing_solutions.exists():
                        raise ValidationError('Вы уже отправляли такое же решение для этого задания')
                except Student.DoesNotExist:
                    pass

        return cleaned_data

    class Meta:
        model = Solution
        fields = ['source_code', 'task']

        widgets = {
            'source_code': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите код решения',
                    'rows': 10,
                }
            ),
        }

from .models import Task, Solution
from django.forms import ModelForm, TextInput, Textarea


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'complexity', 'description']

        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя задания',
                }
            ),
            'complexity': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Сложность задания',
                }
            ),
            'description': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Текст задания',
                }
            ),
        }

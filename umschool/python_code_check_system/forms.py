from django.forms import ModelForm, Textarea, TextInput
from django.forms import inlineformset_factory

from .models import Solution, Task, Test

TestFormSet = inlineformset_factory(Task, Test, fields=('input_data', 'output_data'), extra=1, can_delete=True)

class TaskForm(ModelForm):
    class Meta:
        model = Task
        # fields = '__all__'
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


class SolutionForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

    class Meta:
        model = Solution
        fields = ['student', 'source_code', 'task']

        # widgets = {
        #     'student': TextInput(
        #         attrs={
        #             'class': 'form-control',
        #             'placeholder': 'student',
        #         }
        #     ),
        #     'source_code': TextInput(
        #         attrs={
        #             'class': 'form-control',
        #             'placeholder': 'source_code',
        #         }
        #     ),
        #     'task': Textarea(
        #         attrs={
        #             'class': 'form-control',
        #             'placeholder': 'task',
        #         }
        #     ),
        # }

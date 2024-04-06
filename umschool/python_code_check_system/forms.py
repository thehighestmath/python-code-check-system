from .models import Task, Solution
from django.forms import ModelForm, TextInput, Textarea


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
        fields = ['student_id', 'source_code', 'task_id']

        # widgets = {
        #     'student_id': TextInput(
        #         attrs={
        #             'class': 'form-control',
        #             'placeholder': 'student_id',
        #         }
        #     ),
        #     'source_code': TextInput(
        #         attrs={
        #             'class': 'form-control',
        #             'placeholder': 'source_code',
        #         }
        #     ),
        #     'task_id': Textarea(
        #         attrs={
        #             'class': 'form-control',
        #             'placeholder': 'task_id',
        #         }
        #     ),
        # }

"""
Tests for forms.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError

from account_service.models import CustomUser, Student
from ..models import Task
from ..forms import TaskForm, SolutionForm


class TaskFormTest(TestCase):
    """Тесты для формы TaskForm."""

    def setUp(self):
        self.valid_data = {'name': 'Test Task', 'complexity': 'easy', 'description': 'This is a test task description'}

    def test_valid_form(self):
        """Тест валидной формы."""
        form = TaskForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_empty_name(self):
        """Тест пустого названия."""
        data = self.valid_data.copy()
        data['name'] = ''
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_whitespace_name(self):
        """Тест названия из пробелов."""
        data = self.valid_data.copy()
        data['name'] = '   '
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_name_starts_with_digit(self):
        """Тест названия, начинающегося с цифры."""
        data = self.valid_data.copy()
        data['name'] = '1Test Task'
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_empty_description(self):
        """Тест пустого описания."""
        data = self.valid_data.copy()
        data['description'] = ''
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_whitespace_description(self):
        """Тест описания из пробелов."""
        data = self.valid_data.copy()
        data['description'] = '   '
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)


class SolutionFormTest(TestCase):
    """Тесты для формы SolutionForm."""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123', is_student=True
        )
        self.student = Student.objects.create(user=self.user)
        self.task = Task.objects.create(name='Test Task', complexity='easy', description='Test description')
        self.valid_data = {'source_code': 'print("Hello, World!")', 'task': self.task.id}

    def test_valid_form(self):
        """Тест валидной формы."""
        form = SolutionForm(data=self.valid_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_empty_source_code(self):
        """Тест пустого кода."""
        data = self.valid_data.copy()
        data['source_code'] = ''
        form = SolutionForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('source_code', form.errors)

    def test_short_source_code(self):
        """Тест слишком короткого кода."""
        data = self.valid_data.copy()
        data['source_code'] = 'print()'
        form = SolutionForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('source_code', form.errors)

    def test_long_source_code(self):
        """Тест слишком длинного кода."""
        data = self.valid_data.copy()
        data['source_code'] = 'print("test")\n' * 2000
        form = SolutionForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('source_code', form.errors)

    def test_whitespace_source_code(self):
        """Тест кода из пробелов."""
        data = self.valid_data.copy()
        data['source_code'] = '   \n  \n  '
        form = SolutionForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('source_code', form.errors)

    def test_single_line_source_code(self):
        """Тест кода из одной строки."""
        data = self.valid_data.copy()
        data['source_code'] = 'print("Hello, World!")'
        form = SolutionForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_no_user_provided(self):
        """Тест формы без пользователя."""
        form = SolutionForm(data=self.valid_data)
        # Форма должна работать и без пользователя
        self.assertTrue(form.is_valid())

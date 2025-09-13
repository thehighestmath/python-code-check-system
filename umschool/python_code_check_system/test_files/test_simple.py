"""
Simple tests without cache dependencies.
"""

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from account_service.models import Student
from ..models import Task, Solution, Test

User = get_user_model()


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    },
    SESSION_ENGINE='django.contrib.sessions.backends.db',
)
class SimpleModelTest(TestCase):
    """Простые тесты моделей без кэша."""

    def test_task_creation(self):
        """Тест создания задания."""
        task = Task.objects.create(name='Test Task', complexity='easy', description='Test description')
        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.complexity, 'easy')
        self.assertTrue(task.is_active)

    def test_solution_creation(self):
        """Тест создания решения."""
        user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123', is_student=True
        )
        student = Student.objects.create(user=user)
        task = Task.objects.create(name='Test Task', complexity='easy', description='Test description')

        solution = Solution.objects.create(student=student, task=task, source_code='print("Hello, World!")')

        self.assertEqual(solution.student, student)
        self.assertEqual(solution.task, task)
        self.assertFalse(solution.is_accepted)

    def test_task_validation(self):
        """Тест валидации задания."""
        task = Task(name='', complexity='easy', description='Test')
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_solution_validation(self):
        """Тест валидации решения."""
        user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123', is_student=True
        )
        student = Student.objects.create(user=user)
        task = Task.objects.create(name='Test Task', complexity='easy', description='Test description')

        solution = Solution(student=student, task=task, source_code='')

        with self.assertRaises(ValidationError):
            solution.full_clean()

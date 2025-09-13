"""
Tests for views.
"""

from django.test import TestCase, Client, override_settings
from django.urls import reverse
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
class TaskHomeListViewTest(TestCase):
    """Тесты для TaskHomeListView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123', is_student=True
        )
        self.task = Task.objects.create(name='Test Task', complexity='easy', description='Test description')
        # Создаем тест для задания
        Test.objects.create(task=self.task, input_data='5\n3', output_data='8')

    def test_anonymous_user_redirected(self):
        """Тест перенаправления анонимного пользователя."""
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_authenticated_user_can_view_tasks(self):
        """Тест доступа авторизованного пользователя к заданиям."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_only_active_tasks_shown(self):
        """Тест отображения только активных заданий."""
        # Создаем неактивное задание
        inactive_task = Task.objects.create(
            name='Inactive Task', complexity='easy', description='Inactive description', is_active=False
        )

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        self.assertNotContains(response, 'Inactive Task')


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    },
    SESSION_ENGINE='django.contrib.sessions.backends.db',
)
class AddSolutionViewTest(TestCase):
    """Тесты для AddSolutionView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123', is_student=True
        )
        self.student = Student.objects.create(user=self.user)
        self.task = Task.objects.create(name='Test Task', complexity='easy', description='Test description')
        # Создаем тест для задания
        Test.objects.create(task=self.task, input_data='5\n3', output_data='8')

    def test_anonymous_user_redirected(self):
        """Тест перенаправления анонимного пользователя."""
        response = self.client.get(reverse('solutions-add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_authenticated_student_can_add_solution(self):
        """Тест добавления решения авторизованным студентом."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('solutions-add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_solution_submission(self):
        """Тест отправки решения."""
        self.client.login(username='testuser', password='testpass123')
        # Создаем студента
        student, created = Student.objects.get_or_create(user=self.user)
        data = {'source_code': 'print("Hello, World!")\nprint("This is a test solution")', 'task': self.task.id}
        response = self.client.post(reverse('solutions-add'), data)
        self.assertIn(response.status_code, [301, 302])  # Перенаправление после успешной отправки

        # Проверяем, что решение создано
        solution = Solution.objects.filter(student=student, task=self.task).first()
        self.assertIsNotNone(solution)
        self.assertIn('Hello, World!', solution.source_code)

    def test_empty_code_rejection(self):
        """Тест отклонения пустого кода."""
        self.client.login(username='testuser', password='testpass123')
        data = {'source_code': '', 'task': self.task.id}
        response = self.client.post(reverse('solutions-add'), data)
        # Форма должна показать ошибки валидации или вернуть 400
        self.assertIn(response.status_code, [200, 400])
        # Проверяем, что решение не создано
        solution = Solution.objects.filter(student=self.student, task=self.task).first()
        self.assertIsNone(solution)

    def test_short_code_rejection(self):
        """Тест отклонения слишком короткого кода."""
        self.client.login(username='testuser', password='testpass123')
        data = {'source_code': 'print()', 'task': self.task.id}
        response = self.client.post(reverse('solutions-add'), data)
        # Форма должна показать ошибки валидации или вернуть 400
        self.assertIn(response.status_code, [200, 400])
        # Проверяем, что решение не создано
        solution = Solution.objects.filter(student=self.student, task=self.task).first()
        self.assertIsNone(solution)


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    },
    SESSION_ENGINE='django.contrib.sessions.backends.db',
)
class SolutionListViewTest(TestCase):
    """Тесты для SolutionListView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123', is_student=True
        )
        self.student = Student.objects.create(user=self.user)
        self.task = Task.objects.create(name='Test Task', complexity='easy', description='Test description')
        self.solution = Solution.objects.create(
            student=self.student, task=self.task, source_code='print("Hello, World!")'
        )

    def test_anonymous_user_redirected(self):
        """Тест перенаправления анонимного пользователя."""
        response = self.client.get(reverse('solutions'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_authenticated_user_can_view_solutions(self):
        """Тест доступа авторизованного пользователя к решениям."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('solutions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_only_user_solutions_shown(self):
        """Тест отображения только решений текущего пользователя."""
        # Создаем другого пользователя и его решение
        other_user = User.objects.create_user(
            username='otheruser', email='other@example.com', password='otherpass123', is_student=True
        )
        other_student = Student.objects.create(user=other_user)
        other_solution = Solution.objects.create(
            student=other_student, task=self.task, source_code='print("Other solution")'
        )

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('solutions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, World!')
        self.assertNotContains(response, 'Other solution')

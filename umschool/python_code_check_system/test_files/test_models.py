"""
Tests for models.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError

from account_service.models import CustomUser, Student
from ..models import Task, Solution, Test


class TaskModelTest(TestCase):
    """Тесты для модели Task."""

    def setUp(self):
        self.task_data = {'name': 'Test Task', 'complexity': 'easy', 'description': 'This is a test task description'}

    def test_task_creation(self):
        """Тест создания задания."""
        task = Task.objects.create(**self.task_data)
        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.complexity, 'easy')
        self.assertTrue(task.is_active)
        self.assertIsNotNone(task.created_at)

    def test_task_str(self):
        """Тест строкового представления задания."""
        task = Task.objects.create(**self.task_data)
        expected = f"{task.name} ({task.get_complexity_display()})"
        self.assertEqual(str(task), expected)

    def test_task_validation_empty_name(self):
        """Тест валидации пустого названия."""
        task = Task(name='', complexity='easy', description='Test description')
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_validation_empty_description(self):
        """Тест валидации пустого описания."""
        task = Task(name='Test', complexity='easy', description='')
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_validation_whitespace_only(self):
        """Тест валидации названия из пробелов."""
        task = Task(name='   ', complexity='easy', description='Test description')
        with self.assertRaises(ValidationError):
            task.full_clean()


class SolutionModelTest(TestCase):
    """Тесты для модели Solution."""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123', is_student=True
        )
        self.student = Student.objects.create(user=self.user)
        self.task = Task.objects.create(name='Test Task', complexity='easy', description='Test description')
        self.solution_data = {'student': self.student, 'task': self.task, 'source_code': 'print("Hello, World!")'}

    def test_solution_creation(self):
        """Тест создания решения."""
        solution = Solution.objects.create(**self.solution_data)
        self.assertEqual(solution.student, self.student)
        self.assertEqual(solution.task, self.task)
        self.assertFalse(solution.is_accepted)
        self.assertIsNotNone(solution.created_at)

    def test_solution_str(self):
        """Тест строкового представления решения."""
        solution = Solution.objects.create(**self.solution_data)
        expected = f"Решение {solution.id} для задания '{self.task.name}'"
        self.assertEqual(str(solution), expected)

    def test_solution_validation_empty_code(self):
        """Тест валидации пустого кода."""
        solution = Solution(student=self.student, task=self.task, source_code='')
        with self.assertRaises(ValidationError):
            solution.full_clean()

    def test_solution_validation_short_code(self):
        """Тест валидации слишком короткого кода."""
        solution = Solution(student=self.student, task=self.task, source_code='print()')
        with self.assertRaises(ValidationError):
            solution.full_clean()

    def test_solution_validation_long_code(self):
        """Тест валидации слишком длинного кода."""
        long_code = 'print("test")\n' * 2000  # Создаем очень длинный код
        solution = Solution(student=self.student, task=self.task, source_code=long_code)
        with self.assertRaises(ValidationError):
            solution.full_clean()


class TestModelTest(TestCase):
    """Тесты для модели Test."""

    def setUp(self):
        self.task = Task.objects.create(name='Test Task', complexity='easy', description='Test description')
        self.test_data = {'task': self.task, 'input_data': '1\n2', 'output_data': '3'}

    def test_test_creation(self):
        """Тест создания теста."""
        test = Test.objects.create(**self.test_data)
        self.assertEqual(test.task, self.task)
        self.assertEqual(test.input_data, '1\n2')
        self.assertEqual(test.output_data, '3')
        self.assertIsNotNone(test.created_at)

    def test_test_str(self):
        """Тест строкового представления теста."""
        test = Test.objects.create(**self.test_data)
        expected = f"Тест для '{self.task.name}'"
        self.assertEqual(str(test), expected)

    def test_test_validation_empty_input(self):
        """Тест валидации пустых входных данных."""
        test = Test(task=self.task, input_data='', output_data='3')
        with self.assertRaises(ValidationError):
            test.full_clean()

    def test_test_validation_empty_output(self):
        """Тест валидации пустых выходных данных."""
        test = Test(task=self.task, input_data='1\n2', output_data='')
        with self.assertRaises(ValidationError):
            test.full_clean()

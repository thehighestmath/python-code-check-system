from django.contrib.auth import get_user_model

from django.test import TestCase

from python_code_check_system.models import Solution, Task, Test
from account_service.models import Student
from python_code_check_system.tasks import check_stundet_code_task
from umschool.celery import app


class SolutionTestCase(TestCase):
    def setUp(self):
        app.conf.update(
            task_always_eager=True,
            task_eager_propagates=True,
        )

    def test_sub_two_numbers(self):
        User = get_user_model()
        user = User.objects.create_user('foo', password='bar', is_student=True)
        student = Student.objects.create(user=user)
        task = Task.objects.create(name='Test task', complexity='1', description='')
        Test.objects.create(task=task, input_data='5\n2', output_data='3')
        solution = Solution.objects.create(
            student=student,
            source_code='''
a = int(input())
b = int(input())
print(a - b)
''',
            task=task,
        )
        check_stundet_code_task.delay(solution.id).get(timeout=10)
        passed_solution = Solution.objects.get(id=solution.id)
        self.assertTrue(passed_solution.is_accepted)

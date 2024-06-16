from django.db import models

from account_service.models import Student


class Solution(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='solution')
    source_code = models.TextField()
    task = models.ForeignKey('Task', on_delete=models.DO_NOTHING)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'


class Task(models.Model):
    name = models.CharField(max_length=255)
    complexity = models.CharField(max_length=10, null=True)
    description = models.TextField()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class Test(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    input_data = models.TextField()
    output_data = models.TextField()

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

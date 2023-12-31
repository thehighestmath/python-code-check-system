from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=75, null=True)
    surname = models.CharField(max_length=75, null=True)
    last_name = models.CharField(max_length=75, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Solution(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    source_code = models.FileField()
    task_id = models.ForeignKey('Task', on_delete=models.DO_NOTHING)
    is_accepted = models.BooleanField()

    class Meta:
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'


class Task(models.Model):
    name = models.CharField(max_length=255)
    complexity = models.CharField(max_length=10, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class Test(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    input_data = models.TextField()
    output_data = models.TextField()

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

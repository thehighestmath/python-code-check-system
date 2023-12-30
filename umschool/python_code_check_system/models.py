from django.db import models


class Student(models.Model):
    id = models.BigIntegerField(primary_key=True)
    solutions = models.ForeignKey('Solution', on_delete=models.SET_NULL, null=True)


class Solution(models.Model):
    id = models.BigIntegerField(primary_key=True)
    source_code = models.TextField()
    task_id = models.ForeignKey('Task', on_delete=models.DO_NOTHING)
    is_accepted = models.BooleanField()


class Task(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    tests = models.ForeignKey('Tests', on_delete=models.CASCADE)


class Tests(models.Model):
    id = models.BigIntegerField(primary_key=True)
    input_data = models.TextField()
    output_data = models.TextField()

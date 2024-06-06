from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='student')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='teacher')
    name = models.CharField(max_length=75, null=True)
    surname = models.CharField(max_length=75, null=True)
    last_name = models.CharField(max_length=75, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from account_service.models import Student


class Solution(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, related_name='solutions'  # Исправлено: было 'solution'
    )
    source_code = models.TextField(
        validators=[
            MinLengthValidator(10, message="Код должен содержать минимум 10 символов"),
            MaxLengthValidator(10000, message="Код не должен превышать 10000 символов"),
        ]
    )
    task = models.ForeignKey('Task', on_delete=models.CASCADE)  # Исправлено: было DO_NOTHING
    is_accepted = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True, help_text="Сообщение об ошибке при проверке кода")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Валидация модели Solution"""
        if not self.source_code or not self.source_code.strip():
            raise ValidationError({'source_code': 'Код не может быть пустым'})

        # Проверяем, что код содержит хотя бы одну строку
        if len(self.source_code.strip().split('\n')) < 1:
            raise ValidationError({'source_code': 'Код должен содержать хотя бы одну строку'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Решение {self.id} для задания '{self.task.name}'"

    class Meta:
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'task']),
            models.Index(fields=['is_accepted']),
            models.Index(fields=['created_at']),
        ]


class Task(models.Model):
    COMPLEXITY_CHOICES = [
        ('easy', 'Легкое'),
        ('medium', 'Среднее'),
        ('hard', 'Сложное'),
    ]

    name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(3, message="Название должно содержать минимум 3 символа"),
            MaxLengthValidator(255, message="Название не должно превышать 255 символов"),
        ],
    )
    complexity = models.CharField(
        max_length=10, choices=COMPLEXITY_CHOICES, default='easy', help_text="Уровень сложности задания"
    )
    description = models.TextField(
        validators=[
            MinLengthValidator(10, message="Описание должно содержать минимум 10 символов"),
            MaxLengthValidator(5000, message="Описание не должно превышать 5000 символов"),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Активно ли задание")

    def clean(self):
        """Валидация модели Task"""
        if not self.name or not self.name.strip():
            raise ValidationError({'name': 'Название не может быть пустым'})

        if not self.description or not self.description.strip():
            raise ValidationError({'description': 'Описание не может быть пустым'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_complexity_display()})"

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['complexity']),
            models.Index(fields=['created_at']),
        ]


class Test(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tests')
    input_data = models.TextField(
        validators=[
            MinLengthValidator(1, message="Входные данные не могут быть пустыми"),
            MaxLengthValidator(1000, message="Входные данные не должны превышать 1000 символов"),
        ],
        help_text="Входные данные для теста (по одному значению на строку)",
    )
    output_data = models.TextField(
        validators=[
            MinLengthValidator(1, message="Выходные данные не могут быть пустыми"),
            MaxLengthValidator(1000, message="Выходные данные не должны превышать 1000 символов"),
        ],
        help_text="Ожидаемые выходные данные (по одному значению на строку)",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Валидация модели Test"""
        if not self.input_data or not self.input_data.strip():
            raise ValidationError({'input_data': 'Входные данные не могут быть пустыми'})

        if not self.output_data or not self.output_data.strip():
            raise ValidationError({'output_data': 'Выходные данные не могут быть пустыми'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Тест для '{self.task.name}'"

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['task']),
        ]

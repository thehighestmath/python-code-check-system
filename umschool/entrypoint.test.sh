#!/bin/bash

# Для тестов не ждем базу данных, так как используем SQLite
echo "Running migrations..."
python manage.py migrate

# Создаем тестового студента
echo "Creating test data..."
python manage.py shell -c "
from account_service.models import CustomUser, Student, Teacher
from python_code_check_system.models import Task, Test

# Создаем тестового студента
if not CustomUser.objects.filter(username='student1').exists():
    student_user = CustomUser.objects.create_user('student1', 'student1@example.com', 'student123')
    student_user.is_student = True
    student_user.save()
    Student.objects.create(user=student_user)
    print('Test student created')

# Создаем тестового учителя
if not CustomUser.objects.filter(username='teacher1').exists():
    teacher_user = CustomUser.objects.create_user('teacher1', 'teacher1@example.com', 'teacher123')
    teacher_user.is_teacher = True
    teacher_user.save()
    Teacher.objects.create(user=teacher_user)
    print('Test teacher created')

# Создаем тестовое задание
if not Task.objects.filter(name='Сложение двух чисел').exists():
    task = Task.objects.create(
        name='Сложение двух чисел',
        complexity='Легкая',
        description='Напишите функцию, которая принимает два числа и возвращает их сумму.'
    )
    
    # Создаем тесты для задания
    Test.objects.create(task=task, input_data='2\n3', output_data='5')
    Test.objects.create(task=task, input_data='10\n20', output_data='30')
    Test.objects.create(task=task, input_data='-5\n3', output_data='-2')
    print('Test task created')
"

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000

exec "$@"

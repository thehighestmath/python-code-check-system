# Generated by Django 4.2.1 on 2024-01-01 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_code_check_system', '0001_squashed_0007_task_complexity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

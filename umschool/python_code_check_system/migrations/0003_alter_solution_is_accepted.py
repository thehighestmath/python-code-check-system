# Generated by Django 5.0.1 on 2024-04-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("python_code_check_system", "0002_rename_tests_test"),
    ]

    operations = [
        migrations.AlterField(
            model_name="solution",
            name="is_accepted",
            field=models.BooleanField(default=False),
        ),
    ]

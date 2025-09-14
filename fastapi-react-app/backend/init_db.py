#!/usr/bin/env python3
"""
Script to initialize the database with sample data.
"""

import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import User, Task, Test
from app.services.auth import AuthService
from app.core.config import settings

# Create tables
from app.core.database import Base

Base.metadata.create_all(bind=engine)


def init_db():
    """Initialize database with sample data."""
    db = SessionLocal()
    auth_service = AuthService()

    try:
        # Create admin user
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=auth_service.get_password_hash("admin123"),
                is_student=False,
                is_active=True,
            )
            db.add(admin_user)
            print("Created admin user")

        # Create test student
        student_user = db.query(User).filter(User.username == "student").first()
        if not student_user:
            student_user = User(
                username="student",
                email="student@example.com",
                hashed_password=auth_service.get_password_hash("student123"),
                is_student=True,
                is_active=True,
            )
            db.add(student_user)
            print("Created student user")

        # Create sample tasks
        task1 = db.query(Task).filter(Task.name == "Сумма двух чисел").first()
        if not task1:
            task1 = Task(
                name="Сумма двух чисел",
                description="Напишите программу, которая принимает два числа и выводит их сумму.\n\nВходные данные: два целых числа, каждое на отдельной строке.\nВыходные данные: одно целое число - сумма введенных чисел.",
                complexity="easy",
                is_active=True,
            )
            db.add(task1)
            db.flush()  # Get the ID

            # Add tests for task1
            test1_1 = Test(task_id=task1.id, input_data="5\n3", output_data="8")
            test1_2 = Test(task_id=task1.id, input_data="-2\n7", output_data="5")
            test1_3 = Test(task_id=task1.id, input_data="0\n0", output_data="0")
            db.add_all([test1_1, test1_2, test1_3])
            print("Created task: Сумма двух чисел")

        task2 = db.query(Task).filter(Task.name == "Факториал").first()
        if not task2:
            task2 = Task(
                name="Факториал",
                description="Напишите программу, которая вычисляет факториал числа n.\n\nВходные данные: одно целое число n (0 ≤ n ≤ 10).\nВыходные данные: факториал числа n.",
                complexity="medium",
                is_active=True,
            )
            db.add(task2)
            db.flush()  # Get the ID

            # Add tests for task2
            test2_1 = Test(task_id=task2.id, input_data="5", output_data="120")
            test2_2 = Test(task_id=task2.id, input_data="0", output_data="1")
            test2_3 = Test(task_id=task2.id, input_data="3", output_data="6")
            db.add_all([test2_1, test2_2, test2_3])
            print("Created task: Факториал")

        task3 = db.query(Task).filter(Task.name == "Числа Фибоначчи").first()
        if not task3:
            task3 = Task(
                name="Числа Фибоначчи",
                description="Напишите программу, которая выводит n-е число Фибоначчи.\n\nВходные данные: одно целое число n (1 ≤ n ≤ 20).\nВыходные данные: n-е число Фибоначчи.",
                complexity="hard",
                is_active=True,
            )
            db.add(task3)
            db.flush()  # Get the ID

            # Add tests for task3
            test3_1 = Test(task_id=task3.id, input_data="1", output_data="1")
            test3_2 = Test(task_id=task3.id, input_data="5", output_data="5")
            test3_3 = Test(task_id=task3.id, input_data="10", output_data="55")
            db.add_all([test3_1, test3_2, test3_3])
            print("Created task: Числа Фибоначчи")

        db.commit()
        print("Database initialized successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()

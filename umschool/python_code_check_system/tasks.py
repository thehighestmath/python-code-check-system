from pathlib import Path
from time import sleep
import logging
import os

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .check_system.core import check
from .check_system.types import DataInOut
from .models import Solution, Test
from .exceptions import SolutionNotFoundError, TaskNotFoundError, CodeExecutionError

BASE_DIR = Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)


@shared_task()
def scheduled_task(t):
    sleep(5)
    r = check(
        f"{BASE_DIR}/python_code_check_system/check_system/main.py",
        [
            DataInOut(input_data=["1", "1"], output_data="2"),
            DataInOut(input_data=["2", "2"], output_data="4"),
            DataInOut(input_data=["3", "4"], output_data="7"),
        ],
    )
    print("SCHEDULED TASK HERE", t, r)


@shared_task()
def check_stundet_code_task(solution_id: int):
    """
    Проверяет код студента на соответствие тестам.

    Args:
        solution_id: ID решения для проверки

    Raises:
        SolutionNotFoundError: Если решение не найдено
        TaskNotFoundError: Если задание не найдено
        CodeExecutionError: Если произошла ошибка при выполнении кода
    """
    try:
        # Получаем решение
        try:
            solution = Solution.objects.get(id=solution_id)
        except ObjectDoesNotExist:
            logger.error(f"Solution with id {solution_id} not found")
            raise SolutionNotFoundError(f"Solution with id {solution_id} not found")

        logger.info(f"Starting code check for solution {solution_id}")

        # Создаем временный файл для кода
        path = f"{BASE_DIR}/python_code_check_system/check_system/main.py"

        try:
            with open(path, 'w', encoding='utf-8') as fp:
                fp.write(solution.source_code)
        except IOError as e:
            logger.error(f"Error writing code to file: {e}")
            raise CodeExecutionError(f"Error writing code to file: {e}")

        # Получаем тесты для задания
        try:
            tests = Test.objects.filter(task_id=solution.task_id)
            if not tests.exists():
                logger.warning(f"No tests found for task {solution.task_id}")
                raise TaskNotFoundError(f"No tests found for task {solution.task_id}")
        except Exception as e:
            logger.error(f"Error getting tests for task {solution.task_id}: {e}")
            raise TaskNotFoundError(f"Error getting tests: {e}")

        # Подготавливаем данные тестов
        tests_data = []
        for test in tests:
            try:
                tests_data.append(
                    DataInOut(
                        input_data=test.input_data.split('\n'),
                        output_data=test.output_data.split('\n'),
                    )
                )
            except Exception as e:
                logger.error(f"Error processing test {test.id}: {e}")
                continue

        if not tests_data:
            logger.error(f"No valid tests found for solution {solution_id}")
            solution.is_accepted = False
            solution.save()
            return

        # Выполняем проверку кода
        try:
            sleep(5)  # TODO: remove this delay. used for emulate execute long task
            result = check(path, tests_data)
            solution.is_accepted = result.verdict
            solution.error_message = result.error_verbose if not result.verdict else None
            solution.save()

            logger.info(f"Code check completed for solution {solution_id}. Result: {result.verdict}")
            if not result.verdict and result.error_verbose:
                logger.warning(f"Code check failed for solution {solution_id}: {result.error_verbose}")

        except Exception as e:
            logger.error(f"Error during code execution for solution {solution_id}: {e}")
            solution.is_accepted = False
            solution.error_message = f"Ошибка выполнения: {str(e)}"
            solution.save()
            raise CodeExecutionError(f"Error during code execution: {e}")

        # Очищаем временный файл
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError as e:
            logger.warning(f"Error removing temporary file: {e}")

    except Exception as e:
        logger.error(f"Unexpected error in check_stundet_code_task: {e}")
        # Пытаемся обновить статус решения в случае ошибки
        try:
            solution = Solution.objects.get(id=solution_id)
            solution.is_accepted = False
            solution.error_message = f"Критическая ошибка: {str(e)}"
            solution.save()
        except:
            pass
        raise

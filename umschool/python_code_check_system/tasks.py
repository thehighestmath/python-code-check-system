from pathlib import Path
from time import sleep

from celery import shared_task

from .check_system.core import check
from .check_system.types import DataInOut
from .models import Solution, Test

BASE_DIR = Path(__file__).resolve().parent.parent


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
    solution = Solution.objects.get(id=solution_id)
    solution.source_code
    path = f"{BASE_DIR}/python_code_check_system/check_system/main.py"
    with open(path, 'w') as fp:
        fp.write(solution.source_code)
    tests_data = []
    tests = Test.objects.filter(task_id=solution.task_id)
    for test in tests:
        tests_data.append(
            DataInOut(
                input_data=test.input_data.split('\n'),
                output_data=test.output_data.split('\n'),
            )
        )
    sleep(5) # TODO: remove this delay. used for emulate execute long task
    r = check(path, tests_data)
    solution.is_accepted = r.verdict
    solution.save()
    print("check_stundet_code_task HERE", r)

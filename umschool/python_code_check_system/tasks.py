from time import sleep
from celery import shared_task
from .check_system.core import check
from .check_system.types import DataInOut


@shared_task()
def scheduled_task(t):
    """Sends an email when the feedback form has been submitted."""
    sleep(10)  # Simulate expensive operation(s) that freeze Django
    r = check(
        f"/home/kirillkry/python-code-check-system/umschool/python_code_check_system/check_system/main.py",  # TODO: этот тот ещё хардкод
        [
            DataInOut(input_data=["1", "1"], output_data="2"),
            DataInOut(input_data=["2", "2"], output_data="4"),
            DataInOut(input_data=["3", "4"], output_data="7"),
        ],
    )
    print("SCHEDULED TASK HERE", t, r)

from time import sleep
from celery import shared_task
from pathlib import Path

from .check_system.core import check
from .check_system.types import DataInOut

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

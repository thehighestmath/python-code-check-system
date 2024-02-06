from time import sleep
from celery import shared_task
from .check_system.core import check

@shared_task()
def send_feedback_email_task(t):
    """Sends an email when the feedback form has been submitted."""
    sleep(10)  # Simulate expensive operation(s) that freeze Django
    r = check(
        f"/home/kirillkry/python-code-check-system/umschool/python_code_check_system/check_system/main.py",
        [("1", "1", "2"), ("2", "2", "4"), ("3", "4", "7")]
    )
    print('qweeqweqweqwe', t, r)
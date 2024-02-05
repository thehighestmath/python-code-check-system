from pathlib import Path
from core import check
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize("filepath, tests, expected_result", [(f"{BASE_DIR}/src/main.py",[("1", "1", "2"), ("2", "2", "4"), ("3", "4", "7")], True)])
def test_check(filepath, tests, expected_result):
    assert check(filepath, tests) == expected_result

from pathlib import Path
import pytest

from python_code_check_system.check_system.core import check
from python_code_check_system.check_system.types import DataInOut

BASE_DIR = Path(__file__).resolve().parent.parent

@pytest.mark.parametrize(
    "filepath, tests",
    [
        (
            f"{BASE_DIR}/tests/sample_src/main_plus.py",
            [
                DataInOut(input_data=["1", "1"], output_data="2"),
                DataInOut(input_data=["2", "2"], output_data="4"),
                DataInOut(input_data=["3", "4"], output_data="7"),
            ],
        )
    ],
)
def test_check_plus(filepath, tests):
    assert check(filepath, tests)


@pytest.mark.parametrize(
    "filepath, tests",
    [
        (
            f"{BASE_DIR}/tests/sample_src/main_sub.py",
            [
                DataInOut(input_data=["1", "1"], output_data="0"),
                DataInOut(input_data=["-2", "-5"], output_data="3"),
                DataInOut(input_data=["3", "4"], output_data="-1"),
            ],
        )
    ],
)
def test_check_minus(filepath, tests):
    assert check(filepath, tests)

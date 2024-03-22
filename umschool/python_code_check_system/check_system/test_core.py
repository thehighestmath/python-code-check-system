from pathlib import Path
import pytest

from .core import check
from .types import DataInOut

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    "filepath, tests",
    [
        (
            f"{BASE_DIR}/check_system/main.py",
            [
                DataInOut(input_data=["1", "1"], output_data="2"),
                DataInOut(input_data=["2", "2"], output_data="4"),
                DataInOut(input_data=["3", "4"], output_data="7"),
            ],
        )
    ],
)
def test_check(filepath, tests):
    assert check(filepath, tests)

from pathlib import Path

import pytest
from python_code_check_system.check_system.core import check
from python_code_check_system.check_system.types import DataInOut

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    "filepath, tests",
    [
        pytest.param(
            f"{BASE_DIR}/tests/sample_src/main_plus.py",
            [
                DataInOut(input_data=["1", "1"], output_data=["2"]),
                DataInOut(input_data=["2", "2"], output_data=["4"]),
                DataInOut(input_data=["3", "4"], output_data=["7"]),
            ],
            id="plus",
        ),
        pytest.param(
            f"{BASE_DIR}/tests/sample_src/main_sub.py",
            [
                DataInOut(input_data=["1", "1"], output_data=["0"]),
                DataInOut(input_data=["-2", "-5"], output_data=["3"]),
                DataInOut(input_data=["3", "4"], output_data=["-1"]),
            ],
            id="sub",
        ),
    ],
)
def test_check_simple_math(filepath, tests):
    assert check(filepath, tests).verdict


@pytest.mark.parametrize(
    "filepath, tests, expected_error",
    [
        pytest.param(
            f"{BASE_DIR}/tests/sample_src/main_syntax_error.py",
            [
                DataInOut(input_data=["1", "1"], output_data=["0"]),
            ],
            "SyntaxError",
            id="syntax-error",
        ),
        pytest.param(
            f"{BASE_DIR}/tests/sample_src/main_memory.py",
            [
                DataInOut(input_data=[], output_data=[]),
            ],
            "MemoryError",
            id="memory-out-error",
        ),
        pytest.param(
            f"{BASE_DIR}/tests/sample_src/main_loop.py",
            [
                DataInOut(input_data=[], output_data=[]),
            ],
            "TimeoutError",
            id="timeout-error",
        ),
    ],
)
def test_check_errors(filepath, tests, expected_error):
    assert check(filepath, tests).error_verbose == expected_error


@pytest.mark.parametrize(
    "filepath, tests",
    [
        pytest.param(
            f"{BASE_DIR}/tests/sample_src/main_eval.py",
            [
                DataInOut(input_data=["1+1"], output_data=["2"]),
            ],
            id="eval-call",
        ),
        pytest.param(
            f"{BASE_DIR}/tests/sample_src/main_exec.py",
            [
                DataInOut(input_data=[], output_data=[]),
            ],
            id="exec-call",
        ),
    ],
)
def test_forbidden_function_call(filepath, tests):
    assert check(filepath, tests).error_verbose == "ForbiddenFunctionCall"


@pytest.mark.parametrize(
    "filepath, tests, expected_error",
    [
        pytest.param(
            f"{BASE_DIR}/tests/sample_src/main_plus.py",
            [
                DataInOut(input_data=["1", "1"], output_data=["2"]),
                DataInOut(input_data=["2", "2"], output_data=["2"]),
                DataInOut(input_data=["3", "4"], output_data=["7"]),
            ],
            "test 2 failed",
            id="plus",
        ),
        pytest.param(
            f"{BASE_DIR}/tests/sample_src/main_sub.py",
            [
                DataInOut(input_data=["1", "1"], output_data=["0"]),
                DataInOut(input_data=["-2", "-5"], output_data=["3"]),
                DataInOut(input_data=["3", "4"], output_data=["0"]),
            ],
            "test 3 failed",
            id="sub",
        ),
    ],
)
def test_check_failed_test(filepath, tests, expected_error):
    result = check(filepath, tests)
    assert not result.verdict
    assert result.error_verbose == expected_error

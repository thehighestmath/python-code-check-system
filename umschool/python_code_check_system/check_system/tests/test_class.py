import pytest

from python_code_check_system.check_system.tests.sample_src.main_class import (
    SumClass,
)
from python_code_check_system.check_system.types import DataArgs


@pytest.mark.parametrize(
    "data_args",
    [
        DataArgs(input_args=[3, 5], output_data=8),
        DataArgs(input_args=[4], input_kwargs={"b": 1}, output_data=5),
        DataArgs(input_kwargs={"a": 1, "b": 2}, output_data=3),
    ],
)
def test_sum_class(data_args: DataArgs):
    obj = SumClass(*data_args.input_args, **data_args.input_kwargs)

    assert obj.sum() == data_args.output_data

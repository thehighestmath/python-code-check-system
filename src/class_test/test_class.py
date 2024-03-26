import pytest
from student_code import Operations

with open("test_values.txt") as file:
    list_tests_values = file.readlines()

length = len(list_tests_values)

tuples = []

for row in list_tests_values:
    test_row = row.replace("\n", "").split()
    test_row = list(map(int, test_row))
    tuple1 = tuple(test_row)
    tuples.append(tuple1)


@pytest.mark.parametrize("a, b, expected_result", tuples)
def test_actions(a, b, expected_result):
    obj = Operations(a, b)

    assert obj.a == a
    assert obj.b == b
    assert obj.sum() == expected_result

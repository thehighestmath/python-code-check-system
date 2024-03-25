import pytest
from student_code import Operations

with open("Test_values.txt") as file:
    list_tests_values = file.readlines()

length = len(list_tests_values)

tuples = []

for i in range (0,length):

    test_row = (list_tests_values[i].replace("\n","")).split()

    for j in range(0, len(test_row)):
        test_row[j] = int(test_row[j])

    tuple1 = tuple(test_row)

    tuples.append(tuple1)

@pytest.mark.parametrize("a, b, expected_result", tuples)
def test_actions(a, b, expected_result):
    obj = Operations(a,b)

    assert obj.a == a

    assert obj.b == b

    assert obj.sum() == expected_result

import pytest
from main import deistvia

with open("znach.txt") as file:
    testznach_spisok = file.readlines()

dlina = len(testznach_spisok)

cortejs = []

for i in range (0,dlina):

    test_ryad = (testznach_spisok[i].replace("\n","")).split()
    cortej = tuple(test_ryad)

    cortejs.append(cortej)

@pytest.mark.parametrize("a, b, expected_result", cortejs)
def test_deistvia(a, b, expected_result):
    obj = deistvia(a,b)

    assert obj.a == a

    assert obj.b == b

    assert obj.sum() == expected_result
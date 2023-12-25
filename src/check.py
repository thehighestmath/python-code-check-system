from importlib import reload
import contextlib
import io
import sys
import pytest

file = open("main.py", 'r')
code = ''
while True:
    line = file.readline()
    if not line:
        break
    code += '\t' + line
code += '\nmain()'
file.close()
with open("main.py", "w") as file:
    file.write(f"def main():\n{code}")

sys.stdin = open('../data/data1.in')

f = io.StringIO()
with contextlib.redirect_stdout(f):
    import main


@pytest.mark.parametrize('data_in,data_out', [
    ('data1.in', 'data1.out'),
    ('data2.in', 'data2.out'),
    ('data3.in', 'data3.out'),
    ('data4_in', 'data4_out'),
])
def test_plus1(data_in, data_out):
    sys.stdin = open(f'../data/{data_in}')

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        reload(main)
    output = f.getvalue().strip()
    expected = open(f'../data/{data_out}').read()
    assert output == expected


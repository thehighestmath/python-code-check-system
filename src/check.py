from importlib import reload
import contextlib
import io
import sys
import pytest
import signal
import timeout_exception

code = 'def main():\n'
with open("main.py", 'r') as file:
    lines = file.readlines()
    for i in lines:
        code += '    ' + i

with open("temp_main.py", "w") as file:
    file.write(code)

sys.stdin = open('../data/data1.in')

f = io.StringIO()
with contextlib.redirect_stdout(f):
    import temp_main

signal.signal(signal.SIGALRM, timeout_exception.timeout_handler)


@pytest.mark.parametrize('data_in,data_out', [
    ('data1.in', 'data1.out'),
    ('data2.in', 'data2.out'),
])
def test_plus1(data_in, data_out):
    signal.alarm(15)
    sys.stdin = open(f'../data/{data_in}')

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        try:
            reload(temp_main.main())
        except timeout_exception as exc:
            print("function call timed out")
        finally:
            signal.alarm(0)
    output = f.getvalue().strip()
    expected = open(f'../data/{data_out}').read()
    assert output == expected

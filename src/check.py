import contextlib
import io
import sys
import pytest
import signal
import timeout_exception
from memory_exception import memory_limit

code = [
    """from import_exception import secure_importer\n
__builtins__['__import__'] = secure_importer\n
def main():\n"""]
with open("main.py", 'r') as file:
    lines = file.readlines()
    code.extend(list(map(lambda line: '    ' + line, lines)))

with open("temp_main.py", "w") as file:
    file.write(''.join(code))

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
    signal.alarm(5)
    memory_limit(5)

    sys.stdin = open(f'../data/{data_in}')

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        try:
            temp_main.main()
        except timeout_exception.TimeoutError as exc:
            sys.stderr.write("\nfunction call timed out\n")
        except MemoryError:
            sys.stderr.write('\nERROR: Memory Exception\n')
            sys.exit(2)
        except SyntaxError:
            sys.stderr.write("\nERROR SyntaxError\n")
        finally:
            signal.alarm(5)
    output = f.getvalue().strip()
    expected = open(f'../data/{data_out}').read()
    assert output == expected

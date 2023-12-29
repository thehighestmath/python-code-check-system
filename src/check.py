import contextlib
import os
import io
import sys
import pytest
import signal
from utils import timeout_handler, memory_limit, sorting_data_files
from exceptions import FunctionUsageError, DataError
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

code = [
    """from utils import secure_importer\n
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

signal.signal(signal.SIGALRM, timeout_handler)

data_files = os.listdir(f"{BASE_DIR}/data")
data_in_files = list(filter(lambda name: re.match(r"data\d+\.in", name), data_files))
data_out_files = list(filter(lambda name: re.match(r"data\d+\.out", name), data_files))

try:
    if len(data_in_files) != len(data_out_files):
        raise DataError("Количетсво вводных данных не совпадает с выводимым")
    sorting_data_files(data_in_files)
    sorting_data_files(data_out_files)
except DataError:
    sys.stderr.write("DataError")
print(f"data_out_files = {data_in_files}\n data_in_files = {data_out_files}")

data_all = list(zip(data_in_files, data_out_files))

@pytest.mark.parametrize('data_in,data_out', data_all)
def test_plus1(data_in, data_out):
    print(f"data_in in test_plus1 = {data_in}")
    signal.alarm(5)
    memory_limit(10)

    sys.stdin = open(f'../data/{data_in}')

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        try:
            with open("temp_main.py", 'r') as fp:
                file_content = fp.read()
                if "eval(" in file_content or "exec(" in file_content:
                    raise FunctionUsageError("Forbidden function call")
            temp_main.main()
        except TimeoutError:
            sys.stderr.write("\nERROR: function call timed out\n")
            sys.exit(1)
        except MemoryError:
            sys.stderr.write('\nERROR: Memory Exception\n')
            sys.exit(2)
        except SyntaxError:
            sys.stderr.write("\nERROR: SyntaxError\n")
            sys.exit(3)
        except FunctionUsageError:
            sys.stderr.write("\nERROR: FunctionUsageError\n")
            sys.exit(4)
        finally:
            signal.alarm(5)
    output = f.getvalue().strip()
    expected = open(f'../data/{data_out}').read().strip()
    assert output == expected

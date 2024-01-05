import contextlib
import io
import os
import re
import signal
import sys
from pathlib import Path

import pytest

from exceptions import DataError, FunctionUsageError
from utils import memory_limit, timeout_handler

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

code = [
    """from utils import secure_importer\n
__builtins__['__import__'] = secure_importer\n
def main():\n"""]

with open("main2.py", 'r') as file:
    lines = file.readlines()
    code.extend(list(map(lambda line: '    ' + line, lines)))

with open("temp_main2.py", "w") as file:
    file.write(''.join(code))

sys.stdin = open('../data2/data1.in')

f = io.StringIO()
with contextlib.redirect_stdout(f):
    import temp_main2

signal.signal(signal.SIGALRM, timeout_handler)

data_files = os.listdir(f"{BASE_DIR}/data")
# print(data_files)
data_in_files = list(filter(lambda name: re.match(r"data\d+\.in", name), data_files))
data_out_files = list(filter(lambda name: re.match(r"data\d+\.out", name), data_files))

data_files2 = os.listdir(f"{BASE_DIR}/data2")
print(data_files2)
data_in_files2 = list(filter(lambda name: re.match(r"data\d+\.in", name), data_files2))
data_out_files2 = list(filter(lambda name: re.match(r"data\d+\.out", name), data_files2))
print(data_in_files2)

if len(data_in_files) != len(data_out_files):
    sys.stderr.write("DataError")
    raise DataError("Количетсво вводных данных не совпадает с выводимым")

if len(data_in_files2) != len(data_out_files2):
    sys.stderr.write("DataError")
    raise DataError("Количетсво вводных данных не совпадает с выводимым")


datas = [
    (x, '') for x in data_in_files
] + [
    (x, '2') for x in data_in_files2
]
# [
#     (data_in_files, ''),
#     (data_in_files2, '2'),
# ]
print(datas)

@pytest.mark.parametrize('data', datas)
def test_plus1(data):
    data_in, file_mixin = data
    data_out = data_in.split('.')[0] + '.out'
    signal.alarm(5)
    memory_limit(256)

    sys.stdin = open(f'../data{file_mixin}/{data_in}')

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        try:
            with open(f"temp_main{file_mixin}.py", 'r') as fp:
                file_content = fp.read()
                if "eval(" in file_content or "exec(" in file_content:
                    raise FunctionUsageError("Forbidden function call")
            if file_mixin == '':
                temp_main.main()
            elif file_mixin == '2':
                temp_main2.main()
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
    expected = open(f'../data{file_mixin}/{data_out}').read().strip()
    assert output == expected

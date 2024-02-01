from exceptions import DataError
from pathlib import Path
import sys
import os
import io
import contextlib
import re
from check import run_tests
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


data_files = os.listdir(f"{BASE_DIR}/data")
data_in_files = list(filter(lambda name: re.match(r"data\d+\.in", name), data_files))
data_out_files = list(filter(lambda name: re.match(r"data\d+\.out", name), data_files))

if len(data_in_files) != len(data_out_files):
    sys.stderr.write("DataError")
    raise DataError("Количетсво вводных данных не совпадает с выводимым")

run_tests(f"{BASE_DIR}/src/temp_main.py", data_in_files)

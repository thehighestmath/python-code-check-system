import contextlib
import io
import signal
import sys
import os
from pathlib import Path
import importlib
import uuid

from python_code_check_system.check_system.exceptions import FunctionUsageError
from python_code_check_system.check_system.types import DataInOut


def check(filepath: str, tests: list[DataInOut]) -> bool:
    uid = str(uuid.uuid4()).replace('-', '')
    file_name = f'{uid}.py'
    code = [
        '''from python_code_check_system.check_system.utils import secure_importer\n
__builtins__['__import__'] = secure_importer\n
def main():\n'''
    ]
    with open(filepath, 'r') as file:
        lines = file.readlines()
        code.extend(list(map(lambda line: '    ' + line, lines)))

    with open(f'python_code_check_system/check_system/{file_name}', 'w') as file:
        file.write(''.join(code))

    true_mas = []
    signal.alarm(5)
    # memory_limit(5)

    module_path = f'python_code_check_system.check_system.{uid}'
    temp_main = importlib.import_module(module_path)

    for test in tests:
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            Path('../data/').mkdir(exist_ok=True)
            with open('../data/data.in', 'w') as fp:
                fp.write('\n'.join(test.input_data))
            try:
                sys.stdin = open('../data/data.in')
                with open(filepath, 'r') as fp:
                    file_content = fp.read()
                    if 'eval(' in file_content or 'exec(' in file_content:
                        raise FunctionUsageError('Forbidden function call')
                temp_main.main()
            except TimeoutError:
                sys.stderr.write('\nERROR: function call timed out\n')
                true_mas.append(False)
                continue
            except MemoryError:
                sys.stderr.write('\nERROR: Memory Exception\n')
                true_mas.append(False)
                continue
            except SyntaxError:
                sys.stderr.write('\nERROR: SyntaxError\n')
                true_mas.append(False)
                continue
            except FunctionUsageError:
                sys.stderr.write('\nERROR: FunctionUsageError\n')
                true_mas.append(False)
                continue
            finally:
                signal.alarm(5)
            actual = f.getvalue().strip()
            expected = test.output_data
            true_mas.append(expected == actual)
    os.remove(f'python_code_check_system/check_system/{file_name}')
    return all(true_mas)

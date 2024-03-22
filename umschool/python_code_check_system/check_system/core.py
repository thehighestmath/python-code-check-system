import contextlib
import io
import signal
import sys
import tempfile
from .exceptions import FunctionUsageError
from .types import DataInOut


def check(filepath: str, tests: list[DataInOut]) -> bool:
    code = [
        '''from .utils import secure_importer\n
__builtins__['__import__'] = secure_importer\n
def main():\n'''
    ]
    with open(filepath, 'r') as file:
        lines = file.readlines()
        code.extend(list(map(lambda line: '    ' + line, lines)))

    with open('python_code_check_system/check_system/temp_main.py', 'w') as file:
        file.write(''.join(code))

    true_mas = []
    signal.alarm(5)
    # memory_limit(5)
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        from python_code_check_system.check_system import temp_main
    for test in tests:
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmpfile:
                tmpfile.write('\n'.join(test.input_data))
                tmpfile.flush()
                tmpfile.seek(0)
                sys.stdin = tmpfile
            try:
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
    return all(true_mas)

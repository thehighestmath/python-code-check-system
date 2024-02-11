import contextlib
import io
import signal
import sys
from exceptions import DataError, FunctionUsageError
from utils import memory_limit, timeout_handler


def check(filepath: str, tests: any) -> bool:
    code = [
        """from utils import secure_importer\n
__builtins__['__import__'] = secure_importer\n
def main():\n"""]
    with open(filepath, 'r') as file:
        lines = file.readlines()
        code.extend(list(map(lambda line: '    ' + line, lines)))

    with open("temp_main.py", "w") as file:
        file.write(''.join(code))

    true_mas = []
    signal.alarm(5)
    # memory_limit(5)
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        import temp_main
    for i in range(len(tests)):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with open("../data/data.in", "w") as fp:
                fp.write(f"{tests[i][0]}\n{tests[i][1]}")
            with open("../data/data.out", "w") as fp:
                fp.write(f"{tests[i][2]}")
            try:
                sys.stdin = open("../data/data.in")
                with open(filepath, 'r') as fp:
                    file_content = fp.read()
                    if "eval(" in file_content or "exec(" in file_content:
                        raise FunctionUsageError("Forbidden function call")
                temp_main.main()
            except TimeoutError:
                sys.stderr.write("\nERROR: function call timed out\n")
                true_mas.append(False)
                continue
            except MemoryError:
                sys.stderr.write('\nERROR: Memory Exception\n')
                true_mas.append(False)
                continue
            except SyntaxError:
                sys.stderr.write("\nERROR: SyntaxError\n")
                true_mas.append(False)
                continue
            except FunctionUsageError:
                sys.stderr.write("\nERROR: FunctionUsageError\n")
                true_mas.append(False)
                continue
            finally:
                signal.alarm(5)
            output = f.getvalue().strip()
            expected = open(f'../data/data.out').read().strip()
            with open(f'../data/data_test', 'w') as fp:
                fp.write(str(expected))
            true_mas.append(expected == output)
    return all(true_mas)

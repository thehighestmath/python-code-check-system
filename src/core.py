import contextlib
import io
import signal
import sys
from pathlib import Path
from exceptions import DataError, FunctionUsageError
from utils import memory_limit, timeout_handler
import temp_main


def check(filepath: str, tests: any) -> bool:
    true_mas = []
    BASE_DIR = Path(__file__).resolve().parent.parent
    signal.alarm(5)
    memory_limit(5)
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        import temp_main
    for i in range(len(tests)):
        try:
            sys.stdin = open(f'../data/{tests[i][0]}')
            with open(f"{BASE_DIR}/src/temp_main.py", 'r') as fp:
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
        expected = open(f'../data/{tests[i][1]}').read().strip()
        true_mas.append(output == expected)
    if False not in true_mas: return True
    return False

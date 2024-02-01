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

signal.signal(signal.SIGALRM, timeout_handler)


def run_tests(file, tests_data):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        import temp_main

    @pytest.mark.parametrize('data_in', tests_data)
    def test_plus1(data_in):
        data_out = data_in.split('.')[0] + '.out'
        signal.alarm(5)
        memory_limit(5)

        sys.stdin = open(f'../data/{data_in}')

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            try:
                with open(file, 'r') as fp:
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

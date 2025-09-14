import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import List

import psutil

from app.core.config import settings


class CheckResult:
    def __init__(self, verdict: bool, error_verbose: str = ""):
        self.verdict = verdict
        self.error_verbose = error_verbose


class DataInOut:
    def __init__(self, input_data: List[str], output_data: List[str]):
        self.input_data = input_data
        self.output_data = output_data


class CodeCheckerService:
    def __init__(self):
        self.memory_limit = settings.MEMORY_LIMIT_MB * 1024 * 1024  # Convert to bytes
        self.time_limit = settings.TIME_LIMIT_SECONDS

    def get_error_name(self, traceback: str) -> str:
        """Extract error type from traceback."""
        error_match = re.search(r'\n(\w+): ', traceback)
        if error_match:
            return error_match.group(1)
        return ''

    def read_file(self, filepath: str) -> str:
        """Read file content."""
        with open(filepath, 'r', encoding='utf-8') as fp:
            return fp.read()

    def are_files_the_same(self, filepath_1: str, filepath_2: str) -> bool:
        """Compare two files content."""
        data1 = self.read_file(filepath_1)
        data2 = self.read_file(filepath_2)
        return data1.strip() == data2.strip()

    def check_forbidden_function_call(self, filepath: str) -> bool:
        """Check for forbidden functions like eval() or exec()."""
        file_content = self.read_file(filepath)
        return 'eval(' in file_content or 'exec(' in file_content

    def check_memory(self, proc: subprocess.Popen) -> str:
        """Monitor process memory usage and time limit."""
        start_time = time.time()

        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > self.time_limit:
                proc.kill()
                return 'TimeoutError'

            try:
                process = psutil.Process(proc.pid)
                memory_use = process.memory_info().rss
            except psutil.NoSuchProcess:
                return ''

            if memory_use > self.memory_limit:
                proc.kill()
                return 'MemoryError'

            retcode = proc.poll()
            if retcode is not None:
                return ''

            time.sleep(0.1)

    def restrict_import(self, filepath: str) -> str:
        """Add import restrictions to the code."""
        file_content = self.read_file(filepath)
        head_file = '''# [BEGIN]
import sys
sys.modules['os'] = None
sys.modules['sys'] = None
del sys
# [END]

'''
        new_filepath = f'{filepath}_new.py'
        with open(new_filepath, 'w', encoding='utf-8') as fp:
            fp.write(head_file + file_content)
        return new_filepath

    def check_code(self, filepath: str, tests: List[DataInOut]) -> CheckResult:
        """Check code against test cases."""
        new_filepath = self.restrict_import(filepath)

        if self.check_forbidden_function_call(new_filepath):
            os.remove(new_filepath)
            return CheckResult(
                verdict=False,
                error_verbose='ForbiddenFunctionCall',
            )

        results = []
        base_dir = f'/tmp/data-{abs(hash(new_filepath))}'
        Path(base_dir).mkdir(exist_ok=True)
        error = ''

        try:
            for i, test in enumerate(tests):
                # Write input data
                with open(f'{base_dir}/data.in', 'w', encoding='utf-8') as fp:
                    fp.write('\n'.join(test.input_data))

                # Write expected output
                with open(f'{base_dir}/data.out.expected', 'w', encoding='utf-8') as fp:
                    fp.write('\n'.join(test.output_data))

                # Run the code
                with (
                    open(f'{base_dir}/data.in', 'r') as stdin_file,
                    open(f'{base_dir}/data.out.actual', 'w') as stdout_file,
                    open(f'{base_dir}/error', 'w') as stderr_file,
                ):

                    process = subprocess.Popen(
                        args=['python3', '-S', new_filepath],
                        stdin=stdin_file,
                        stdout=stdout_file,
                        stderr=stderr_file,
                    )

                # Check memory and time limits
                if out := self.check_memory(process):
                    error = out
                    break

                # Check for errors
                if err := self.read_file(f'{base_dir}/error'):
                    error = self.get_error_name(err)
                    break

                # Compare outputs
                result = self.are_files_the_same(f'{base_dir}/data.out.expected', f'{base_dir}/data.out.actual')
                results.append(result)

                if not result:
                    error = f'test {i + 1} failed'
                    break

        finally:
            # Cleanup
            if os.path.exists(new_filepath):
                os.remove(new_filepath)
            if os.path.exists(base_dir):
                shutil.rmtree(base_dir)

        if error:
            results.append(False)

        return CheckResult(
            verdict=all(results),
            error_verbose=error,
        )

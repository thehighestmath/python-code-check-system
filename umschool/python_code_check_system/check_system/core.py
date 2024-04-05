import re
import os
import subprocess
import shutil
from pathlib import Path

from python_code_check_system.check_system.types import DataInOut, CheckResult


def get_error_name(traceback: str) -> str:
    error_match = re.search(r'\n(\w+): ', traceback)

    if error_match:
        error_type = error_match.group(1)
        return error_type
    return ''


def read_file(filepath: str) -> str:
    with open(filepath) as fp:
        return fp.read()


def are_file_the_same(filepath_1: str, filepath_2: str) -> bool:
    data1 = read_file(filepath_1)
    data2 = read_file(filepath_2)
    return data1.strip() == data2.strip() # TODO: fix .strip()


def check(filepath: str, tests: list[DataInOut]) -> CheckResult:
    true_mas = []
    base_dir = f'./data-{abs(hash(filepath))}'
    error = ''
    for test in tests:
        Path(base_dir).mkdir(exist_ok=True)
        with open(f'{base_dir}/data.in', 'w') as fp:
            fp.write('\n'.join(test.input_data))
        with open(f'{base_dir}/data.out.expected', 'w') as fp:
            fp.write('\n'.join(test.output_data))
        # os.system(f'python3 -S {filepath} < {base_dir}/data.in > {base_dir}/data.out.actual 2> {base_dir}/error')
        process = subprocess.Popen(['python3', '-s', filepath, '<', f'{base_dir}/data.in', '>', f'{base_dir}/data.out.actual', '2>', f'{base_dir}/error'])
        try:
            print('Running in process', process.pid)
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print('Timed out - killing', process.pid)
            process.kill()
        print("Done")
        if err := read_file(f'{base_dir}/error'):
            error = get_error_name(err)
            break
        else:
            true_mas.append(are_file_the_same(f'{base_dir}/data.out.expected', f'{base_dir}/data.out.actual'))
    shutil.rmtree(base_dir)
    return CheckResult(
        verdict=all(true_mas),
        error_verbose=error,
    )

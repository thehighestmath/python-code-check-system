import re
import shutil
import subprocess
import time
from pathlib import Path

import psutil
from python_code_check_system.check_system.types import CheckResult, DataInOut


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


def check_forbidden_function_call(filepath: str) -> str:
    file_content = read_file(filepath)
    return 'eval(' in file_content or 'exec(' in file_content


def check_memory(proc: subprocess.Popen) -> bool:
    # TODO: these params must be specified with task
    MEMORY_LIMIT = 100 * 1024 * 1024 # 100MB
    TIME_LIMIT = 1
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > TIME_LIMIT:
            proc.kill()
            return 'TimeoutError'

        try:
            process = psutil.Process(proc.pid)
            memory_use = process.memory_info().rss
        except psutil.NoSuchProcess:
            return ''

        if memory_use > MEMORY_LIMIT:
            proc.kill()
            return 'MemoryError'

        retcode = proc.poll()
        if retcode is not None:
            return ''

        time.sleep(0.5)


def check(filepath: str, tests: list[DataInOut]) -> CheckResult:
    if check_forbidden_function_call(filepath):
        return CheckResult(
            verdict=False,
            error_verbose='ForbiddenFunctionCall',
    )

    true_mas = []
    base_dir = f'./data-{abs(hash(filepath))}'
    error = ''
    for test in tests:
        Path(base_dir).mkdir(exist_ok=True)
        with open(f'{base_dir}/data.in', 'w') as fp:
            fp.write('\n'.join(test.input_data))
        with open(f'{base_dir}/data.out.expected', 'w') as fp:
            fp.write('\n'.join(test.output_data))
        process = subprocess.Popen(
            args=['python3', '-S', filepath],
            stdin=open(f'{base_dir}/data.in'),
            stdout=open(f'{base_dir}/data.out.actual', 'w'),
            stderr=open(f'{base_dir}/error', 'w'),
        )
        if out := check_memory(process):
            error = out
        if err := read_file(f'{base_dir}/error'):
            error = get_error_name(err)
            break
        true_mas.append(are_file_the_same(f'{base_dir}/data.out.expected', f'{base_dir}/data.out.actual'))
    shutil.rmtree(base_dir)
    if error != '':
        true_mas.append(False)
    return CheckResult(
        verdict=all(true_mas),
        error_verbose=error,
    )

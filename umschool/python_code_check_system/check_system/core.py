import os
from pathlib import Path

from python_code_check_system.check_system.types import DataInOut


def read_file(filepath: str) -> str:
    with open(filepath) as fp:
        return fp.read()


def are_file_the_same(filepath_1: str, filepath_2: str) -> bool:
    data1 = read_file(filepath_1)
    data2 = read_file(filepath_2)
    return data1.strip() == data2.strip() # TODO: fix .strip()


def check(filepath: str, tests: list[DataInOut]) -> bool:
    true_mas = []
    for test in tests:
        Path('./data/').mkdir(exist_ok=True)
        with open('./data/data.in', 'w') as fp:
            fp.write('\n'.join(test.input_data))
        with open('./data/data.out.expected', 'w') as fp:
            fp.write('\n'.join(test.output_data))
        os.system(f'python3 -S {filepath} < ./data/data.in > ./data/data.out.actual 2> ./data/error')
        if read_file('./data/error') != '':
            true_mas.append(False)
        else:
            true_mas.append(are_file_the_same('./data/data.out.expected', './data/data.out.actual'))
    return all(true_mas)

from python_code_check_system.check_system.utils import secure_importer

__builtins__['__import__'] = secure_importer

def main():
    a = int(input())
    b = int(input())
    print(a - b)

import resource
import importlib


def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    frommodule = globals['__name__'] if globals else None
    if name in ("os", "sys") and frommodule not in ("os", "sys"):
        raise ImportError(f"module {name} is restricted.")

    return importlib.__import__(name, globals, locals, fromlist, level)


def memory_limit(n: int):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (n * 1024 * 1024, hard))


def timeout_handler(signum, frame):
    raise TimeoutError("function call timed out")


def sorting_data_files(data_files):
    for index_name, name in enumerate(data_files):
        for element in name:
            if element.isdigit():
                index = int(element) - 1
                temp = data_files[index]
                data_files[index] = name
                data_files[index_name] = temp

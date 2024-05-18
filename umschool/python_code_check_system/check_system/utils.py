import importlib
import resource


def secure_importer(name, globals_=None, locals_=None, fromlist=(), level=0):
    frommodule = globals_['__name__'] if globals_ else None
    if name in ("os", "sys") and frommodule not in ("os", "sys"):
        raise ImportError(f"module {name} is restricted.")

    return importlib.__import__(name, globals_, locals_, fromlist, level)


def memory_limit(n: int):
    _, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (n * 1024 * 1024, hard))


def timeout_handler(signum, frame):
    raise TimeoutError("function call timed out")

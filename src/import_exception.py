import importlib


def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    frommodule = globals['__name__'] if globals else None
    if name in ("os", "sys") and frommodule not in ("os", "sys"):
        raise ImportError(f"module {name} is restricted.")
    return importlib.__import__(name, globals, locals, fromlist, level)

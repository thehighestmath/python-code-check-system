import importlib


def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    if name != 'os' and name != 'sys':
        print(name, fromlist, level)

    from_module = globals['__name__'] if globals else None
    if name in ("os", "sys") and from_module not in ("os", "sys"):
        raise ImportError(f"module {name} is restricted.")

    return importlib.__import__(name, globals, locals, fromlist, level)


__builtins__.__dict__['__import__'] = secure_importer

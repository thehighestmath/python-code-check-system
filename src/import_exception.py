import importlib


def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    if name != 'os' and name != 'sys':
        print(name, fromlist, level)

    if name == "os" or name == "sys":
        raise ImportError(f"module {name} is restricted.")

    return importlib.__import__(name, globals, locals, fromlist, level)



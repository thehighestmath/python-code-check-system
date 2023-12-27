import importlib


def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    #if name != 'os' and name != 'sys':

    frommodule = globals['__name__'] if globals else None
    if name == "os" or name == "sys" and frommodule != "os" and frommodule != "sys" and name == "xyz":
        raise ImportError(f"module {name} is restricted.")

    return importlib.__import__(name, globals, locals, fromlist, level)


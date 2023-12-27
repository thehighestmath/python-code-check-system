# import importlib
#
#
# def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
#     if name != 'os' and name != 'sys':
#         print(name, fromlist, level)
#
#     frommodule = globals['__name__'] if globals else None
#     if name == "os" or name == "eval" or name == "exec":
#         raise ImportError("module '%s' is restricted." % name)
#
#     return importlib.__import__(name, globals, locals, fromlist, level)
#
#
# __builtins__.__dict__['__import__'] = secure_importer

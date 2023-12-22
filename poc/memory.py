"""
https://stackoverflow.com/questions/46327566/how-to-have-pytest-place-memory-limits-on-tests
"""
import resource, os, psutil  # pip install psutil
import numpy


def memory_limit(max_mem):
    def decorator(f):
        def wrapper(*args, **kwargs):
            process = psutil.Process(os.getpid())
            prev_limits = resource.getrlimit(resource.RLIMIT_AS)
            print(prev_limits)
            print(process.memory_info().rss)
            resource.setrlimit(resource.RLIMIT_AS, (max_mem, -1))
            result = f(*args, **kwargs)
            resource.setrlimit(resource.RLIMIT_AS, prev_limits)
            return result

        return wrapper

    return decorator


@memory_limit(int(1e16)) # bytes. 1e16 ok. 1e6 fail
def allocate(N):
    return numpy.arange(N, dtype="u8")


a = [allocate(int(1e8)) for i in range(10)]

try:
    allocate(int(3e8))
except:
    exit(0)

raise Exception("Should have failed")

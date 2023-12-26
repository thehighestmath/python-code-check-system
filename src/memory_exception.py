import resource, os, psutil
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
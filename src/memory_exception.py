import resource


def memory_limit(n: int):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (n * 1024 * 1024, hard))

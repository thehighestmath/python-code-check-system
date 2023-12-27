class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("function call timed out")

class timeoutexception(Exception):
    pass


def timeout_handler(signum, frame):
    raise timeoutexception("function call timed out")

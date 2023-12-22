"""
https://stackoverflow.com/questions/492519/timeout-on-a-function-call
https://stackoverflow.com/questions/47545002/python-standard-lib-signal-attributeerror-module-signal-has-no-attribute
"""
def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    import signal
    class TimeoutError(Exception):
        pass
    def handler(signum, frame):
        raise TimeoutError()
    # set the timeout handler
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)
    return result


def loop():
    import time
    while True:
        print('qwe')
        time.sleep(0.1)


timeout(loop)

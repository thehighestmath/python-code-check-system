from memory_exception import memory_limit
@memory_limit(int(15e6))
def main():
    s = 'qwe'
    while True:
        s += s
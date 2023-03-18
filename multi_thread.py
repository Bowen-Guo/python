"""Multi-thread program demo."""


from concurrent import futures
from time import sleep
from contextvars import ContextVar

from timer import Timer

MAX_WORKERS = 20


def sleep_seconds(n: int):
    sleep(n)
    print('Week up!')


def count_down(n: int):
    n_ini = n
    while n > 0:
        n -= 1

    print(f'Count down from {n_ini} to 0 finishes!')


class Foo:    
    def __init__(self):
        self._name = None

    def set_name_and_print(self, name: str):
        self._name = name
        sleep(1)
        self.print()

    def print(self):
        print(f'name = {self._name}')


class ThreadSafeFoo:
    def __init__(self):
        self._name = ContextVar('name', default=None)

    def set_name_and_print(self, name: str):
        self._name.set(name)
        sleep(1)
        self.print()

    def print(self):
        print(f'name = {self._name.get()}')


def demo_sleep_parallelism():
    with Timer('sleep_seconds'):
        sleep_seconds(5)   # Take about 5 seconds
   
    with Timer('sleep_seconds in parallel'):  # Take about 5 seconds
        n_thread = 5
        with futures.ThreadPoolExecutor(min(n_thread, MAX_WORKERS)) as executor:
            result = executor.map(sleep_seconds, [5] * 5)


def demo_countdown_parallelism():
    n  = 50000000
    with Timer(f'Count down from {n}'):  # Take about 2.5 seconds
        count_down(n)

    with Timer('sleep_seconds in parallel'):  # Take about 11.64 seconds. Multi-thread cannot achieve parallelism for cpu-bound operation.
        n_thread = 5
        with futures.ThreadPoolExecutor(min(n_thread, MAX_WORKERS)) as executor:
            result = executor.map(count_down, [n] * 5)


def demo_thread_safety():
    with futures.ThreadPoolExecutor(2) as executor:
        foo = Foo()
        result = executor.map(foo.set_name_and_print, ['name 1', 'name 2'])  # Both thread prints name 2

        foo = ThreadSafeFoo()
        result = executor.map(foo.set_name_and_print, ['name 1', 'name 2'])  # Print name 1 and name 2 respectively


def main():
    demo_sleep_parallelism()

    demo_countdown_parallelism()

    demo_thread_safety()
    

if __name__ == '__main__':
    main()
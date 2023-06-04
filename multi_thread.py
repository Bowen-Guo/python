"""Multi-thread program demo."""

import multiprocessing
from concurrent import futures
from time import sleep
from contextvars import ContextVar
from threading import Thread

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


def sleep_seconds(n: int, i: int):
    sleep(n)
    print(f'i = {i}')


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


def print_or_show_exception(i: int):
    print(f'input i = {i}')
    if i == 0:
        raise Exception('i == 0')

    sleep(5)
    print(f'i = {i}')
    return i


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


def demo_exception_handling():
    try:
        t1 = Thread(target=print_or_show_exception, args=[0])
        t2 = Thread(target=print_or_show_exception, args=[1])
        t1.start()
        t2.start()
        t1.join()  # Throw exception
        t2.join()  # continue running
    except Exception as ex:
        print(f'Catch exception when testing thread. Exception: {ex}')

    try:
        # Test ThreadPoolExecutor.map
        with futures.ThreadPoolExecutor(2) as executor:
            result = executor.map(print_or_show_exception, [0, 1])  # Exception will not be thrown here    
        for r in result:
            print(r)  # Exceptions will be thrown when the result value is retrieved. Need to add try catch here.
    except Exception as ex:
        print(f'Catch exception when testing ThreadPoolExecutor.map. Exception: {ex}')

    try:
        # Test ThreadPoolExecutor.submit
        with futures.ThreadPoolExecutor(2) as executor:
            future1 = executor.submit(print_or_show_exception, 0)
            future2 = executor.submit(print_or_show_exception, 1)

            print(future1.result())  # Execption will be thrown here.
            print(future2.result())
    except Exception as ex:
        print(f'Catch exception when testing ThreadPoolExecutor.submit. Exception: {ex}')


def demo_executor_map_multiple_args():
    l = [(5, 1), (5, 2), (5, 3)]
    with Timer(f'Thread pool'):   # Take about 5 seconds.
        with multiprocessing.Pool(processes=len(l)) as pool:
            result = pool.starmap(sleep_seconds, l)  
    

def main():
    demo_sleep_parallelism()

    demo_countdown_parallelism()

    demo_thread_safety()

    demo_exception_handling()

    demo_executor_map_multiple_args()

if __name__ == '__main__':
    main()
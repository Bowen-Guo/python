# Illustrate python thread utility.

import time
from threading import Thread


def sleep(seconds: float):
    time.sleep(seconds)


def sleep_in_another_thread():
    thread = Thread(target=sleep, args=[10])
    thread.start()
    thread.join(1)


def sleep_in_another_daemon_thread():
    thread = Thread(target=sleep, args=[10])
    thread.daemon = True
    thread.start()
    thread.join(1)


def main():
    # sleep_in_another_thread()  # Main process only exit if this thread has finished.
    sleep_in_another_daemon_thread()  # Main process exists before daemon thread has finished.


if __name__ == '__main__':
    main()

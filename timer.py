import time

class Timer:
    def __init__(self, name: str):
        self._start_time = None
        self._name = name

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise Exception(f"Timer {self._name} is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise Exception(f"Timer {self._name} is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"[{self._name}] Elapsed time: {elapsed_time:0.4f} seconds")

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()
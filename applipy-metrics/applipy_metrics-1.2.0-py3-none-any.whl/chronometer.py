import time


class Chronometer:
    def __init__(self, clock=time, on_stop=None):
        super().__init__()
        self.clock = clock
        self.start_time = self.clock.time()
        self.on_stop = on_stop

    def stop(self):
        elapsed = self.clock.time() - self.start_time

        if self.on_stop:
            self.on_stop(elapsed)

        return elapsed

    def __enter__(self):
        self.start_time = self.clock.time()

    def __exit__(self, t, v, tb):
        self.stop()

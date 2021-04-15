import threading
import time


class AutoReloadMixin:
    def auto_reload(self, interval: int = 60 * 10):
        def x():
            while True:
                self.fetch()
                time.sleep(interval)

        t = threading.Thread(target=x)
        t.setDaemon(True)
        t.start()

    def fetch(self):
        raise NotImplemented

import sys
import time
from collections import deque


class _Spinner:
    spinners = {
        'classic': (['|', '/', '-', '\\'], 0.1),
        'dots': (['▫ ▫ ▫', '▪ ▫ ▫', '▫ ▪ ▫', '▫ ▫ ▪'], 0.2),
        'equal': (['⁼ ⁼ ⁼', '= ⁼ ⁼', '⁼ = ⁼', '⁼ ⁼ ='], 0.2),

        'braille': (['⠏', '⠹', '⠼', '⠧'], 0.1),
        'braille_long': (['⡏', '⢹', '⣸', '⣇'], 0.1),
        'braille_crawl': (['⠌', '⠒', '⠡', '⠨'], 0.1),
        'braille_bounce': (['⣶', '⣭', '⠿', '⣭'], 0.1),
        'arc': (['◜', '◝', '◞', '◟'], 0.1),
        'clear_quadrants': (['◴', '◷', '◶', '◵'], 0.1),
    }

    def __iter__(self):
        self._count = 0
        return self

    def __next__(self):
        if self._count < self._spinner_len:
            spinner_instance = self._spinner[self._count]
            self._count += 1
            return spinner_instance
        raise StopIteration

    def __init__(self, style, interval=None):
        self._style = style or 'classic'

        try:
            spinner_group = self.spinners[self._style]
        except KeyError:
            spinner_group = self.spinners['classic']
        self._spinner, self.interval = spinner_group

        self._spinner_len = len(self._spinner)


class VisualExample:
    def __enter__(self):
        self.deque = deque([], maxlen=self.maxlen)
        self.count = 1
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return

    def __init__(self):
        self.maxlen = len(_Spinner.spinners)
        self.deque = deque(
            [(_Spinner.spinners[i][0], i) for i in _Spinner.spinners], maxlen=self.maxlen)

        self.count = 0

    def close(self):
        try:
            if self.deque:
                self.deque.clear()
        except AttributeError:
            pass
        return

    def start(self):
        count = 0
        while True:
            for _ in range(len(self.deque)):
                sys.stdout.write('\033[1A\033[K')
            string = ' {} style={}'
            strings = [string.format(spinner[count], text)
                       for spinner, text in self.deque]
            for string in strings:
                sys.stdout.write('{}\n'.format(string))
            count += 1
            if count > 3:
                count = 0
            time.sleep(0.1)

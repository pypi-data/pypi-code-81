import platform
import threading
import time
import traceback
import types

from .spinner import Spinner


class Revolution:
    def __call__(self, *args, **kwargs):
        """
        Allows `Revolution` to be called as a function decorator.
        """

        # If the decorator doesn't have any arguments:
        if hasattr(self, '_func'):
            self.start()
            self._func(*args, **kwargs)
            self._event.set()
            while not self._spin_event.is_set():
                pass
        # ...otherwise, the function is in *args:
        else:
            func = args[0]
            if isinstance(func, types.FunctionType):
                def wrapper(*margs, **mkwargs):
                    if not hasattr(self, '_spin_event'):
                        self.start()

                    func(*margs, **mkwargs)

                    if self._total:
                        self._count += 1
                        if self._total == self._count:
                            while not self._spin_event.is_set():
                                pass
                    else:
                        self._event.set()
                        while not self._spin_event.is_set():
                            pass
                return wrapper

    def __enter__(self):
        """
        Entry point for with statements. Used in conjunction with __exit__.
        """

        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Exit point for with statements. Used in conjunction with __enter__.
        """

        self._event.set()
        if (exc_type, exc_value, exc_traceback) == (None, None, None):
            while not self._spin_event.is_set():
                pass
            return
        traceback.print_exception(exc_type, exc_value, exc_traceback)

    def __iter__(self):
        """
        Allows for loops to be used with Revolution objects. Used in conjunction with
        __next__.
        """

        self.start()
        return self

    def __next__(self):
        """
        Used in conjunction with with __iter__.
        """

        # If the for loop was given an iterable such as a list:
        if hasattr(self, '_iter'):
            if self._count < self._stop:
                return_value = self._iter[self._count]
                self._count += self._step
                return return_value
            raise StopIteration
        # otherwise, it's likely a range object and so:
        else:
            if self._count < self._stop:
                return_value = self._count
                self._count += self._step
                return return_value
            raise StopIteration

    def __init__(self, func=None, desc='', total=None, style='', safe=True,
                 interval=None):
        """
        FUNC

        The `func` parameter may seem a little odd but it's necessary in order to be able
        to use a Revolution object as a function decorator and as an iterable or through a
        with statement. 

        The `func` parameter should be left blank unless you initialize a Revolution object
        with a range object or a list.

        -----
        DESC

        The `desc` parameter accepts a string object that will be displayed alongside the
        visual spinner. 

        -----
        TOTAL

        The `total` parameter accepts an integer value that will be used as the total number
        of expected iterations.

        It's recommended that you do not include this value when using a Revolution object as
        a function decorator. The exception to this is if the decorated function is the target
        of a concurrency operation (for example: concurrent.futures).

        For use as a decorator, ensuring you have the correct total specified is crucial. For
        with statements, it is not.

        -----
        STYLE

        The `style` parameter accepts a string object that will be used to specify the spinner
        style. If `style` is None or if it doesn't exist, the classic style will be used.

        -----
        SAFE

        The `safe` parameter accepts a bool value that will use a spinner style that is safe
        for terminals on Windows machines.

        Often, certain spinner styles (such as any of the Braille styles) will appear as 
        boxed-in question marks in CMD and PowerShell if the user is using the default font 
        for those applications. If you are using a certain spinner style and are unsure as to
        how it will appear on Windows machines, it is recommended that you leave `safe` set to
        its default value, True.

        -----
        INTERVAL

        The `interval` paremeter accepts a float value indicating how often the spinner should
        refresh.
        """

        if func:
            # If `func` is provided a range object or list:
            if isinstance(func, range) or isinstance(func, list):
                try:
                    self._count = func.start
                    self._stop = func.stop
                    self._step = func.step

                    self._total = func.end
                except AttributeError:
                    self._count = 0
                    self._stop = len(func)
                    self._step = 1
                    self._iter = func

                    self._total = self._stop
            # ...otherwise, it must be a FunctionType:
            else:
                self._func = func
                self._count = 0
                self._total = total
        else:
            self._count = 0
            self._total = total

        self._desc = desc

        # Determines which spinner style should be used based on the OS:
        if safe:
            if platform.system() == 'Windows':
                self._style = 'classic'
            else:
                self._style = style or 'classic'
        else:
            self._style = style or 'classic'
        self._spinner = Spinner(self._style, interval)
        self._interval = self._spinner.interval

        self._rate = 0

    def start(self):
        self._event = threading.Event()
        thread = threading.Thread(target=self._spin)
        if not self._total:
            thread.setDaemon(True)
        thread.start()

    def stop(self):
        if not self._event.is_set():
            self._event.set()

    def update(self, step=1):
        self._count += step

    def _spin(self):
        # For preventing premature ejection:
        self._spin_event = threading.Event()

        rate_thread = threading.Thread(target=self._update_rate)
        rate_thread.setDaemon(True)
        rate_thread.start()

        statement = self._make_statement()

        while True:
            for spinner in self._spinner:
                print('\r', end='')
                print(statement.format(
                    spinner, self._desc, self._count, self._total, self._rate),
                    end='', flush=False)
                if self._event.is_set() or self._count == self._total:
                    print()
                    self._spin_event.set()
                    return
                time.sleep(self._interval)

    def _make_statement(self):
        if self._total:
            statement = ' {} {} [{}/{}] ({})    '
        else:
            statement = ' {} {}    '
        return statement

    def _update_rate(self):
        if self._total:
            last_time = time.perf_counter()
            previous_count = self._count
            while True:
                self._rate = f'{round((self._count - previous_count) / (time.perf_counter() - last_time), 4)} it/s'
                last_time = time.perf_counter()
                previous_count = self._count
                time.sleep(0.5)

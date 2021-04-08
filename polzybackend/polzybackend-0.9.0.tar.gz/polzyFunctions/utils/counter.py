import threading

lock = threading.Lock()  # to make class thread safe


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Counter(metaclass=Singleton):
    """
    This is a singleton class to provide antragnummer. It takes care of providing unique number/id.
    """
    def __init__(self):
        from polzybackend.models import AntragNummer  # importing table here to avoid import error
        self.AntragNummer = AntragNummer              # To avoid importing this table on every method call we made it
        self.number = self.AntragNummer.get_count()                                                 # class attribute

    def get_number(self):
        number = self.number
        self.number += 1
        if self.number % 100 == 0:            # if number is divisible by 100 update value in db with 100
            self.AntragNummer.update_count()
        return number

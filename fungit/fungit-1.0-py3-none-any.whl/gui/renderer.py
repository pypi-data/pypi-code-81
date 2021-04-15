import threading
from typing import Dict


class Renderer:
    """Holds the draw buffer and manages IO blocking queue
    * .buffer([+]name[!], *args, append=False, now=False, z=100) : Add *args to buffer
    * - Adding "+" prefix to name sets append to True and appends to name's current string
    * - Adding "!" suffix to name sets now to True and print name's current string
    * .out(clear=False) : Print all strings in buffer, clear=True clear all buffers after
    * .now(*args) : Prints all arguments as a string
    * .clear(*names) : Clear named buffers, all if no argument
    """

    idle = threading.Event()
    idle.set()

    old_tree: Dict = dict()  # for diff
    _w: int = 0
    _h: int = 0
    _is_changed: bool = False

    @classmethod
    def now(cls, *args):
        """Wait for input reader and self to be idle then print to screen"""
        cls.idle.wait()
        cls.idle.clear()
        try:
            print(*args, sep="", end="", flush=True)
        except BlockingIOError:
            pass
            print(*args, sep="", end="", flush=True)
        cls.idle.set()

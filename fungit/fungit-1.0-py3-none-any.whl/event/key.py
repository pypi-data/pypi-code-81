import threading
import tty
import termios
import fcntl
import os
import sys
from time import sleep, time
from select import select
from typing import List, Dict, Tuple, Union


class Timer:
    timestamp: float
    return_zero = False

    @classmethod
    def stamp(cls):
        cls.timestamp = time()

    @classmethod
    def not_zero(cls) -> bool:
        if cls.return_zero:
            cls.return_zero = False
            return False
        return cls.timestamp + (1) > time()

    @classmethod
    def left(cls) -> float:
        return cls.timestamp + (1) - time()

    @classmethod
    def finish(cls):
        cls.return_zero = True
        cls.timestamp = time() - (1)
        Key.break_wait()


class Raw(object):
    """Set raw input mode for device"""

    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()

    def __enter__(self):
        self.original_stty = termios.tcgetattr(self.stream)
        tty.setcbreak(self.stream)

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)


class Nonblocking(object):
    """Set nonblocking mode for device"""

    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()

    def __enter__(self):
        self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)

    def __exit__(self, *args):
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)


class Key:
    """Handles the threaded input reader for keypresses and mouse events"""

    list: List[str] = []
    mouse: Dict[str, List[List[int]]] = {}
    mouse_pos: Tuple[int, int] = (0, 0)
    escape: Dict[Union[str, Tuple[str, str]], str] = {
        "\n": "enter",
        ("\x7f", "\x08"): "backspace",
        ("[A", "OA"): "up",
        ("[B", "OB"): "down",
        ("[D", "OD"): "left",
        ("[C", "OC"): "right",
        "[2~": "insert",
        "[3~": "delete",
        "[H": "home",
        "[F": "end",
        "[5~": "page_up",
        "[6~": "page_down",
        "\t": "tab",
        "[Z": "shift_tab",
        "OP": "f1",
        "OQ": "f2",
        "OR": "f3",
        "OS": "f4",
        "[15": "f5",
        "[17": "f6",
        "[18": "f7",
        "[19": "f8",
        "[20": "f9",
        "[21": "f10",
        "[23": "f11",
        "[24": "f12",
    }
    new = threading.Event()
    idle = threading.Event()
    mouse_move = threading.Event()
    mouse_report: bool = False
    idle.set()
    stopping: bool = False
    started: bool = False
    reader: threading.Thread

    @classmethod
    def start(cls):
        cls.stopping = False
        cls.reader = threading.Thread(target=cls._get_key)
        cls.reader.start()
        cls.started = True

    @classmethod
    def stop(cls):
        if cls.started and cls.reader.is_alive():
            cls.stopping = True
            try:
                cls.reader.join()
            except:
                pass

    @classmethod
    def last(cls) -> str:
        if cls.list:
            return cls.list.pop()
        else:
            return ""

    @classmethod
    def get(cls) -> str:
        if cls.list:
            return cls.list.pop(0)
        else:
            return ""

    @classmethod
    def get_mouse(cls) -> Tuple[int, int]:
        if cls.new.is_set():
            cls.new.clear()
        return cls.mouse_pos

    @classmethod
    def mouse_moved(cls) -> bool:
        if cls.mouse_move.is_set():
            cls.mouse_move.clear()
            return True
        else:
            return False

    @classmethod
    def has_key(cls) -> bool:
        return bool(cls.list)

    @classmethod
    def clear(cls):
        cls.list = []

    @classmethod
    def input_wait(cls, sec: float = 0.0, mouse: bool = False) -> bool:
        """Returns True if key is detected else waits out timer and returns False"""
        if cls.list:
            return True
        # if mouse:
        # Draw.now(Term.mouse_direct_on)
        cls.new.wait(sec if sec > 0 else 0.0)
        # if mouse:
        # Draw.now(Term.mouse_direct_off, Term.mouse_on)

        if cls.new.is_set():
            cls.new.clear()
            return True
        else:
            return False

    @classmethod
    def break_wait(cls):
        cls.list.append("_null")
        cls.new.set()
        sleep(0.01)
        cls.new.clear()

    @classmethod
    def _get_key(cls):
        """Get recive keys.

        Get a key or escape sequence from stdin, convert to readable format
        and save to keys list. Meant to be run in it's own thread.
        """
        input_key: str = ""
        clean_key: str = ""
        try:
            while not cls.stopping:
                with Raw(sys.stdin):
                    # * Wait 100ms for input on stdin then restart loop to check for stop flag
                    if not select([sys.stdin], [], [], 0.1)[0]:
                        continue
                    # * Read 1 key safely with blocking on
                    input_key += sys.stdin.read(1)
                    if (
                        input_key == "\033"
                    ):  # * If first character is a escape sequence keep reading
                        # * Report IO block in progress to prevent Draw functions from getting a IO Block error
                        cls.idle.clear()
                        # Draw.idle.wait()  # * Wait for Draw function to finish if busy
                        # * Set non blocking to prevent read stall
                        with Nonblocking(sys.stdin):
                            input_key += sys.stdin.read(20)
                            print(input_key)
                            if input_key.startswith("\033[<"):
                                _ = sys.stdin.read(1000)
                        cls.idle.set()  # * Report IO blocking done
                    # errlog.debug(f'{repr(input_key)}')
                    if input_key == "\033":
                        clean_key = (
                            "escape"  # * Key is "escape" key if only containing \033
                        )
                    # * Detected mouse event
                    elif input_key.startswith(
                        ("\033[<0;", "\033[<35;", "\033[<64;", "\033[<65;")
                    ):
                        try:
                            cls.mouse_pos = (
                                int(input_key.split(";")[1]),
                                int(input_key.split(";")[2].rstrip("mM")),
                            )
                        except:
                            pass
                        else:
                            # * Detected mouse move in mouse direct mode
                            if input_key.startswith("\033[<35;"):
                                cls.mouse_move.set()
                                cls.new.set()
                            # * Detected mouse scroll up
                            elif input_key.startswith("\033[<64;"):
                                clean_key = "mouse_scroll_up"
                            # * Detected mouse scroll down
                            elif input_key.startswith("\033[<65;"):
                                clean_key = "mouse_scroll_down"
                            # * Detected mouse click release
                            elif input_key.startswith(
                                "\033[<0;"
                            ) and input_key.endswith("m"):
                                if False:
                                    clean_key = "mouse_click"
                                else:
                                    for (
                                        key_name,
                                        positions,
                                    ) in (
                                        cls.mouse.items()
                                    ):  # * Check if mouse position is clickable
                                        if list(cls.mouse_pos) in positions:
                                            clean_key = key_name
                                            break
                                    else:
                                        clean_key = "mouse_click"
                    elif input_key == "\\":
                        clean_key = "\\"  # * Clean up "\" to not return escaped
                    else:
                        for (
                            code
                        ) in (
                            cls.escape.keys()
                        ):  # * Go trough dict of escape codes to get the cleaned key name
                            if input_key.lstrip("\033").startswith(code):
                                clean_key = cls.escape[code]
                                break
                        else:  # * If not found in escape dict and length of key is 1, assume regular character
                            if len(input_key) == 1:
                                clean_key = input_key
                    if clean_key:
                        # * Store up to 10 keys in input queue for later processing
                        cls.list.append(clean_key)
                        if len(cls.list) > 10:
                            del cls.list[0]
                        clean_key = ""
                        cls.new.set()  # * Set threading event to interrupt main thread sleep
                    input_key = ""

        except Exception as e:
            # errlog.exception(f'Input thread failed with exception: {e}')
            cls.idle.set()
            cls.list.clear()
            # clean_quit(1, thread=True)

__all__ = ("_enter", "_exit", "_verify")


_counter = 0


def _enter(*args, **kwds) -> None:
    global _counter
    _counter += 1


def _exit() -> None:
    global _counter
    assert _counter > 0
    _counter -= 1


def _verify() -> bool:
    global _counter
    return _counter > 0

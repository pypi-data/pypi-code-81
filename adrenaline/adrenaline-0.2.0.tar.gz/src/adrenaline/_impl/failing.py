__all__ = ("_enter", "_exit", "_verify")


def _enter(*args, **kwds) -> None:
    raise NotImplementedError("Not supported on this platform")


def _verify() -> bool:
    return False


_exit = _enter

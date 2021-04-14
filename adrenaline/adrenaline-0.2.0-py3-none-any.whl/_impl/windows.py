import ctypes

__all__ = ("_enter", "_exit", "_verify")

# The following constants are from
# https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

_previous_state = None


def _enter(*, display: bool, reason: str) -> None:
    global _previous_state

    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    if display:
        flags |= ES_DISPLAY_REQUIRED

    previous_state = ctypes.windll.kernel32.SetThreadExecutionState(flags)
    if previous_state is None:
        raise RuntimeError("Failed to call SetThreadExecutionState()")

    _previous_state = previous_state


def _exit() -> None:
    assert _previous_state is not None
    ctypes.windll.kernel32.SetThreadExecutionState(_previous_state)


def _verify() -> bool:
    previous_state = ctypes.windll.kernel32.SetThreadExecutionState(0)
    if previous_state is None:
        raise RuntimeError("Failed to call SetThreadExecutionState()")
    ctypes.windll.kernel32.SetThreadExecutionState(previous_state)
    return bool(previous_state & (ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED))

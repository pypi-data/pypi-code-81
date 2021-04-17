"""Module with utilities to log messages and display them in a dialog."""

# Standard library:
import os

# local:
from jarpyvscode.log import logger

NOGUI: bool = bool(os.getenv("TESTRUN", "0"))

try:
    # Standard library:
    import tkinter
    from tkinter import messagebox
except ModuleNotFoundError:
    logger.warning("Cannot import 'tkinter'. GUI messages disabled.")


def error(message: str) -> None:
    """Log an error message and show an error dialog."""
    logger.error(message)
    if not NOGUI:
        try:
            # try block since the function may be called from
            # a non Main Thread.
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showerror("JAR's pyVSCode", message)
            root.destroy()
        except Exception:
            pass


def info(message: str) -> None:
    """Log an information message and show an info dialog."""
    logger.info(message)
    if not NOGUI:
        try:
            # try block since the function may be called from
            # a non Main Thread.
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showinfo("JAR's pyVSCode", message)
            root.destroy()
        except Exception:
            pass


def warning(message: str) -> None:
    """Log a warning message and show a warning dialog."""
    logger.warning(message)
    if not NOGUI:
        try:
            # try block since the function may be called from
            # a non Main Thread.
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showwarning("JAR's pyVSCode", message)
            root.destroy()
        except Exception:
            pass

"""Separate module with helper to avoid cycled imports."""

# Standard library:
import os


def is_insiders() -> bool:
    """Determine if the Visual Studio Code Insiders build is in use

    Returns
    -------
    bool
        True, when the Visual Studio Code Insiders build is in use

    """
    return bool(int(os.getenv("IS_INSIDERS", "0")))

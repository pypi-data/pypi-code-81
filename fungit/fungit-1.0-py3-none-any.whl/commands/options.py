from .exec import run_with_git


def stage(*args) -> None:
    """Stage files."""

    command = "add --"
    s = run_with_git(" ".join([command, *args])).rstrip()


def stage_all() -> None:
    """Stage all files."""

    run_with_git("add -A")


def unstage(*args, tracked: bool = True) -> None:
    """Unstage files."""

    if tracked:
        command = "reset HEAD --"
    else:
        command = "rm --cached --force --"

    run_with_git(" ".join([command, *args]))


def unstage_all() -> None:
    """Unstage all files."""

    run_with_git("reset")


def pull():

    run_with_git("pull")

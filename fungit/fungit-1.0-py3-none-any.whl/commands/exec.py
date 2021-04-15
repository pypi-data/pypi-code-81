import subprocess

_GIT = "git"


def run_with_git(*args) -> str:
    """Execute a git command and return the result.

    Args:
        args: Command parameter tuple

    Returns:
        Execution result, string text
    """

    c = " ".join([_GIT, *args])
    # print(c)
    try:
        with subprocess.Popen([c], stdout=subprocess.PIPE, shell=True) as proc:
            return proc.stdout.read().decode()
    except Exception as e:
        print(e)
        return ""

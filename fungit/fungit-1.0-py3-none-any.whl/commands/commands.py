import os

from .exec import run_with_git


def current_head():
    return run_with_git("symbolic-ref -q --short HEAD").strip()


def state() -> list:
    """Get current project name and head branch."""

    path = run_with_git("rev-parse --git-dir").strip()
    if path == ".git":
        project = os.getcwd().split("/")[-1]
    else:
        project = path.split("/")[-2]

    _head = current_head()
    return [project, _head]


def branch_log(branch) -> str:
    """Gets all logs of a given branch.

    Args:
        branch: branch name
    """

    # if branch.startswith('* '):
    #     branch = branch[2:]
    branch_name = branch.name

    arg = "log %s --graph --decorate" % branch_name
    resp = run_with_git(arg).rstrip()
    return resp


def commit_info(commit: str) -> str:
    """Gets the information for a given submission.

    Args:
        commit: commit id
    """

    return commit_file_info(commit)


def commit_file_info(commit: str, file_name: str = "") -> str:
    """Gets the change of a file in a given commit.

    Args:
        commit: commit id
        file_name: file name(include full path)
    """

    arg = "show %s %s" % (commit, file_name)
    resp = run_with_git(arg).rstrip()
    return resp


def stashs() -> str:
    """Get stash list."""

    arg = "stash list"
    resp = run_with_git(arg)
    return resp


def diff(file: str, tracked: bool = True, cached: bool = False) -> str:
    """Get the diff of given file.

    Args:
        file: file path
        tracked: Is the file tracked
        cached: Is the file staged
    """

    args = ["diff", "--submodule", "--no-ext-diff"]
    if cached:
        args.append("--cached")

    if not tracked:
        args.append("--no-index -- /dev/null")
    else:
        args.append("--")

    args.append(file)

    res = run_with_git(*args).rstrip()
    return res


def is_selected_branch(branch: str) -> bool:
    """Determine whether a branch is the current branch."""

    return branch.startswith("* ")


# TODO: just temp introduce
INTRODUCE = """\
A terminal tool, help you use git more simple. Support Linux and MacOS.
   
Usage: g <option> [<args>]

You can use `-h` and `--help` to get how to use pyzgit.
"""

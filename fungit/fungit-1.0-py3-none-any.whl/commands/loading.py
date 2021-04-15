import re
from typing import List

from .exec import run_with_git
from .module.file import File
from .module.branch import Branch
from .module.commit import Commit


def load_files(*args) -> List[File]:
    """Get all file.

    Returns a list of `File` based on the current branch or head.

    Args:
        args: File tuple
    """

    command = "status -s -u"
    resp = run_with_git(" ".join([command, *args])).rstrip()

    files_ = []
    if resp:
        lines_ = resp.split("\n")
        for line_ in lines_:
            # _status.append((item[:2], item[3:]))
            change = line_[:2]
            staged_change = line_[:1]
            unstaged_change = line_[1:2]
            name = line_[3:]
            untracked = change in ["??", "A ", "AM"]
            has_no_staged_change = staged_change in [" ", "U", "?"]
            has_merged_conflicts = change in ["DD", "AA", "UU", "AU", "UA", "UD", "DU"]
            has_inline_merged_conflicts = change in ["UU", "AA"]

            file_ = File(
                name=name,
                display_str=line_,
                short_status=change,
                has_staged_change=not has_no_staged_change,
                has_unstaged_change=unstaged_change != " ",
                tracked=not untracked,
                deleted=unstaged_change == "D" or staged_change == "D",
                added=unstaged_change == "A" or untracked,
                has_merged_conflicts=has_merged_conflicts,
                has_inline_merged_conflicts=has_inline_merged_conflicts,
            )
            files_.append(file_)

    return files_


def load_branches() -> List[Branch]:
    command = 'for-each-ref --sort=-committerdate --format="%(HEAD)|%(refname:short)|%(upstream:short)|%(upstream:track)" refs/heads'
    resp = run_with_git(command).strip()

    if not resp:
        return []

    branchs = []
    lines = resp.split("\n")

    for line in lines:
        items = line.split("|")
        branch = Branch(
            name=items[1], pushables="?", pullables="?", is_head=items[0] == "*"
        )

        upstream_name = items[2]

        if not upstream_name:
            branchs.append(branch)
            continue

        branch.upstream_name = upstream_name

        track = items[3]
        _re = re.compile(r"ahead (\d+)")
        match = _re.search(track)
        if match:
            branch.pushables = str(match[1])
        else:
            branch.pushables = "0"

        _re = re.compile(r"behind (\d+)")
        match = _re.search(track)
        if match:
            branch.pullables = str(match[1])
        else:
            branch.pullables = "0"

        branchs.append(branch)

    return branchs


def get_first_pushed_commit(branch_name: str):
    command = "merge-base %s %s@{u}" % (branch_name, branch_name)
    resp = run_with_git(command).strip()
    return resp


def get_log(branch_name: str, limit: bool = False, filter_path: str = ""):
    limit_flag = "-300" if limit else ""
    filter_flag = f"--follow -- {filter_path}" if filter_path else ""
    command = f'log {branch_name} --oneline --pretty=format:"%H|%at|%aN|%d|%p|%s" {limit_flag} --abbrev=20 --date=unix {filter_flag}'
    resp = run_with_git(command).strip()
    return resp


def load_commits(branch_name: str):
    """Return given branch all commits.

    Args:
        branch_name: A string of branch name.
    """

    passed_first_pushed_commit = False
    first_pushed_commit = get_first_pushed_commit(branch_name)

    if not first_pushed_commit:
        passed_first_pushed_commit = True

    commits = []
    lines = get_log(branch_name).split("\n")
    for line in lines:
        split_ = line.split("|")

        sha = split_[0]
        unix_timestamp = int(split_[1])
        author = split_[2]
        extra_info = (split_[3]).strip()
        parent_hashes = split_[4]
        message = "|".join(split_[5:])

        tag = []
        if extra_info:
            _re = re.compile(r"tag: ([^,\\]+)")
            match = _re.search(extra_info)
            if match:
                tag.append(match[1])

        if sha == first_pushed_commit:
            passed_first_pushed_commit = True
        status = {True: "unpushed", False: "pushed"}[not passed_first_pushed_commit]

        commit_ = Commit(
            sha=sha,
            msg=message,
            author=author,
            unix_timestamp=unix_timestamp,
            status=status,
            extra_info=extra_info,
            tag=tag,
        )
        commits.append(commit_)

    return commits

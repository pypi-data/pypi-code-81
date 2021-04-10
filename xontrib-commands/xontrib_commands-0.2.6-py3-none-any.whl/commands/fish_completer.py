from xonsh.completers import completer
from xonsh.completers.tools import RichCompletion

from .utils import run


def create_rich_completion(line: str):
    line = line.strip()
    if "\t" in line:
        cmd, desc = map(str.strip, line.split("\t", maxsplit=1))
    else:
        cmd, desc = line, ""
    return RichCompletion(
        str(cmd),
        description=str(desc),
        style="bg:#cbf7f4 fg:ansiblack",
    )


def fish_proc_completer(prefix: str, line: str, begidx, endidx, ctx):
    """Populate completions using fish shell and remove bash-completer"""
    output = run("fish", "-c", f"complete -C '{line}'")
    print(output, "---")
    return set(map(create_rich_completion, output.strip().splitlines(keepends=False)))


completer.add_one_completer(
    "fish",
    fish_proc_completer,
    # "start"
)
completer.remove_completer("bash")

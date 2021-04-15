from .gitoptions import GIT_OPTIONS
from .shared import echo, run_shell_with_resp, warn, err, Color, Style


def echo_one_help_msg(k: str):
    echo("    " + k, color=Color.GREEN, nl=False)
    if GIT_OPTIONS[k]["help-msg"]:
        msg = GIT_OPTIONS[k]["help-msg"]
    else:
        msg = GIT_OPTIONS[k]["command"]
    echo((9 - len(k)) * " " + str(msg))


def echo_help_msg(keys: list):
    echo("Usage: g <option> [<args>]\n", style=Style.BOLD)
    # echo('')
    if keys:
        invalid_keys = []
        for k in keys:
            if GIT_OPTIONS.get(k):
                echo_one_help_msg(k)
            else:
                invalid_keys.append(k)
        if invalid_keys:
            echo("\nDont support these options: ", nl=False)
            echo(" ".join(invalid_keys), color=Color.RED)
    else:
        echo(
            """
-h / --help [<args>]  :get help mesage, default is all.
                       You can also follow the parameters to 
                       get help information for specific commands.

--complete            :You can use this option to get shell auto completion.
                       Just support `bash`, `zsh`.
        """
        )
        echo("These are short commands that can replace git operations:")
        for k in GIT_OPTIONS.keys():
            echo_one_help_msg(k)


def give_tip(c: str):
    err("Don't support option: {}".format(c))
    echo("\nMaybe what you want is:")
    c = c[0]
    for k in GIT_OPTIONS.keys():
        if k.startswith(c):
            echo_one_help_msg(k)


def echo_description():
    from .version import VERSION

    has_git = False
    try:
        git_veriosn = run_shell_with_resp("git --version")
        has_git = True
    except Exception as e:
        git_veriosn = ""

    echo("[pyzgit] version: %s" % VERSION, style=Style.BOLD)
    echo(" " + git_veriosn + "\n")
    echo(
        "A terminal tool, help you use git more simple. Support Linux and MacOS.\n",
        style=Style.UNDERLINE,
    )

    echo("Usage: g <option> [<args>]", style=Style.BOLD)
    echo("You can use ", nl=False)
    echo("-h", color=Color.GREEN, nl=False)
    echo(" and ", nl=False)
    echo("--help", color=Color.GREEN, nl=False)
    echo(" to get how to use pyzgit.\n")

    if not has_git:
        warn("Dont found Git, maybe need install.")

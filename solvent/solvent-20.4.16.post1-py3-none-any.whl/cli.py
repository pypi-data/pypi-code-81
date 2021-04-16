import itertools
import pdb
import sys

import log
import pomace
import typer
from bullet import Bullet

from .scripts import Script


def run():
    typer.run(cli)


def cli(
    names: list[str] = typer.Argument(
        None,
        metavar="[SCRIPT SCRIPT ...]",
        help="Names of one or more scripts to run in a loop",
    ),
    duration: int = typer.Option(
        5 * 60, metavar="SECONDS", help="Amount of time to spend in each script"
    ),
    dev: bool = typer.Option(False, help="Enable development mode"),
):
    log.init()

    scripts = {}
    for cls in Script.__subclasses__():
        script = cls()  # type: ignore
        scripts[script.name] = script

    choices = list(scripts.keys())
    if "all" in names:
        log.info("Running all scripts")
        names = ["donjr", "mypillow", "stopstacey"]

    cli = Bullet(prompt="\nSelect a script to run:", bullet=" ● ", choices=choices)
    if not all(name in choices for name in names) or not names:
        names = [cli.launch()]
        pomace.prompts.linebreak(force=True)

    try:
        import caffeine
    except ImportError:
        log.warn(f"Display sleep cannot be disabled on {sys.platform}")
    else:
        caffeine.on(display=True)

    pomace.utils.locate_models()
    if not dev:
        pomace.freeze()

    try:
        _run(scripts, names, duration)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log.error(e)
        if dev:
            extype, value, tb = sys.exc_info()
            pdb.post_mortem(tb)
        else:
            raise e from None


def _run(scripts: dict, names: list, duration: int):
    if len(names) > 1:
        for count in itertools.count(start=1):
            for name in names:
                scripts[name].loop(duration)
    else:
        scripts[names[0]].loop()

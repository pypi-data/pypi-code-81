#!/usr/bin/python3
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlparse

import requests
import yaml


#############
# Constants #
#############
COLORS = {
    "exception": "\033[1;31m",
    "error": "\033[1;31m",
    "warning": "\033[1;33m",
    "info": "\033[1;37m",
    "debug": "\033[0;37m",
    "target": "\033[32m",
    "input": "\033[0;35m",
    "feedback": "\033[0;33m",
    "results": "\033[1;34m",
    "dt": "\033[0;90m",
    "end": "\033[0m",
}


###########
# Helpers #
###########
def download(src, dst):
    url = urlparse(src)
    if url.scheme in ["http", "https"]:
        ret = requests.get(src)
        dst.write_text(ret.text, encoding="utf-8")
    else:
        shutil.copyfile(src, dst)


##########
# Setups #
##########
def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tuxrun", description="TuxRun")

    group = parser.add_argument_group("configuration files")
    group.add_argument("--device", required=True, help="Device configuration")
    group.add_argument("--definition", required=True, help="Job definition")

    group = parser.add_argument_group("docker")
    group.add_argument("--docker", default=None, help="Docker image")
    group.add_argument(
        "--pull", default=False, action="store_true", help="Force a docker pull"
    )

    parser.add_argument(
        "--log-file", default=None, type=Path, help="Store logs to file"
    )

    return parser


##############
# Entrypoint #
##############
def _main(options, tmpdir: Path) -> int:
    # Download if needed and copy to tmpdir
    download(str(options.device), (tmpdir / "device.yaml"))
    download(str(options.definition), (tmpdir / "definition.yaml"))

    args = [
        "lava-run",
        "--device",
        str(tmpdir / "device.yaml"),
        "--job-id",
        "1",
        "--output-dir",
        "output",
        str(tmpdir / "definition.yaml"),
    ]

    # Add docker if needed
    if options.docker:
        # docker pull on demand
        if options.pull:
            subprocess.call(["docker", "pull", options.docker])
        docker = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{tmpdir}:{tmpdir}",
            "-v",
            "/boot:/boot:ro",
            "-v",
            "/lib/modules:/lib/modules:ro",
            "--hostname",
            "tuxrun",
            options.docker,
        ]
        args = docker + args

    # Should we write lava-run logs to a file
    log_file = None
    if options.log_file is not None:
        log_file = options.log_file.open("w")

    try:
        proc = subprocess.Popen(args, bufsize=1, stderr=subprocess.PIPE, text=True)
        assert proc.stderr is not None
        for line in proc.stderr:
            line = line.rstrip("\n")
            try:
                data = yaml.load(line, Loader=yaml.CFullLoader)  # type: ignore
                if not data:
                    continue
                if log_file is not None:
                    log_file.write("- " + line + "\n")
                else:
                    level = data["lvl"]
                    msg = data["msg"]
                    timestamp = data["dt"].split(".")[0]

                    sys.stdout.write(
                        f"{COLORS['dt']}{timestamp}{COLORS['end']} {COLORS[level]}{msg}{COLORS['end']}\n"
                    )
            except (yaml.YAMLError, KeyError):
                sys.stdout.write(line + "\n")
            sys.stdout.flush()
        return proc.wait()
    except FileNotFoundError as exc:
        sys.stderr.write(f"File not found '{exc.filename}'\n")
        return 1
    except Exception:
        proc.kill()
        outs, errs = proc.communicate()
        # TODO: do something with outs and errs
        raise
    return 0


def main() -> int:
    # Parse command line
    options = setup_parser().parse_args()

    # Create a temp directory
    tmpdir = Path(tempfile.mkdtemp(prefix="tuxrun-"))
    try:
        return _main(options, tmpdir)
    finally:
        shutil.rmtree(tmpdir)


def start():
    if __name__ == "__main__":
        sys.exit(main())


start()

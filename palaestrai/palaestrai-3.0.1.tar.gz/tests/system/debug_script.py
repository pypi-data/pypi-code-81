from palaestrai.cli.manager import cli
from tests.system.test_cli import runtime_path, debug_script_path

if __name__ == "__main__":
    cli(["-c", runtime_path, "-vv", "experiment-start", debug_script_path])

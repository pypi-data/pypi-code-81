import subprocess
import logging

logger = logging.getLogger(__name__)


def run_shell_command(command: str):
    """Given a string of a bash command, run the shell command here. This is risky AF, so make sure you are careful and don't use this to accept user input."""
    args = command.split(" ")
    response = subprocess.Popen(args=args)
    logger.info(f"{command} response: {response}")

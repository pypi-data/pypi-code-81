import subprocess


def subprocess_run(command, input_=None):
    """Run the given command as if it were run in a command line."""
    if isinstance(command, str):
        command_list = command.split(' ')
    else:
        command_list = command

    process = subprocess.run(command_list, input=input_, text=True, capture_output=True)
    result = (process.stdout, process.stderr)
    return result

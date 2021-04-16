import subprocess
from typing import List


class ProcessUtil:
    """
    """

    @staticmethod
    def execute(
        command: List[str], cwd: str = "./", stdout: int = subprocess.PIPE
    ) -> int:
        """
        runs a given command to completion using subprocess then
        returns the return code

        Args:
            command (List[str]): the command to run, where each element in the list
                is either a command or its arguments
            cwd (str): the directory to run this command in
            stdout (int): the file to write the output to
        """
        process = subprocess.Popen(
            command, cwd=cwd, stdout=stdout, stderr=subprocess.PIPE
        )
        process.communicate()
        return process.returncode

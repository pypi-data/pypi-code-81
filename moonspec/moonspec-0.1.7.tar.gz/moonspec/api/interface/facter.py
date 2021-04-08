import json
import logging
import shutil
import subprocess

LOGGER = logging.getLogger('moonspec')


class FacterApi:
    """
    Interface to `facter` utility.
    """

    @staticmethod
    def is_supported() -> bool:
        """
        Check if `facter` utility is found on current host.

        :return: True if facter is found on current host, False otherwise
        """
        return shutil.which('facter') is not None

    @staticmethod
    def get_facts() -> dict:
        """
        Retrieve facts about host operating system using `facter` utility.

        :return: facter command output as dict
        """
        cmd = ['facter', '-j']

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE)
        except BaseException as e:
            LOGGER.error('Failed to execute facter', exc_info=e)
            return {}

        if 0 is not result.returncode:
            return {}

        return json.loads(result.stdout)

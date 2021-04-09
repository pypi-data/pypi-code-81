import re
import subprocess as sp
from os import path
from typing import List


class ExceptionSOEM(Exception):
    pass


class SOEMMaster:

    def __init__(self, interface: str):
        """
        Init SOEM Master.
        Parameters
        ----------
        interface : str
            Name of interface
        """
        self._if = interface

    def get_slave_info(self, pdo_map: bool = False, sdos: bool = False) -> List[str]:
        """
        Get slave info.

        Parameters
        ----------
        pdo_map : bool
            Print PDO Mapping
        sdos : bool
            Print SDOs

        Returns
        -------
        List[str]
            List with slave infos
        """
        option = ""
        if pdo_map:
            option += " -map"

        if sdos:
            option += " -sdo"

        command = f"sudo slaveinfo {self._if} {option}"
        state_string = sp.check_output(command,
                                       universal_newlines=True,
                                       shell=True)
        slave_info = re.findall(r'(Slave:\d+.+?)^(\n|End)', state_string, re.DOTALL | re.MULTILINE)

        return [i[0].replace("\n ", "\n") for i in slave_info]

    def get_slave_short_info(self, slaveid: int = 0) -> str:
        """
        Get slave short info by slave ID.
        Parameters
        ----------
        slaveid : int
            Slave ID

        Returns
        -------
        str
            Slave Info
        """
        command = f"sudo eepromtool {self._if} {slaveid + 1} -i"
        state_string = sp.check_output(command,
                                       universal_newlines=True,
                                       shell=True)
        return state_string

    def get_slave_count(self) -> int:
        """
        Get amount of connected slaves.

        Returns
        -------
        int
            Amount of connected slaves.
        """
        state_string = self.get_slave_short_info()

        res = re.search(r'(\d+) slaves found', state_string, re.MULTILINE)
        if res:
            return int(res.group(1))
        return 0

    # SOEM slave ID starts at 1, IgH at 0
    def sii_write(self, filepath: str = "somanet_cia402.sii", hex_string: bool = False, slaveid: int = 0) -> bool:
        """
        Write SII file to slave.

        Parameters
        ----------
        filepath : str
            Path to SII file.
        hex_string : bool
            File is in Hex String format. Default is binary.
        slaveid : int
            Slave ID

        Returns
        -------
        bool
            True, if successfully written.
        """
        if path.exists(filepath) == False:
            raise ExceptionSOEM(f"Error file '{filepath}' not found.")

        option = "-w"
        if hex_string:
            option += "i"

        command = f"sudo eepromtool {self._if} {slaveid + 1} {option} {filepath}"
        return sp.call(command, stdout=sp.DEVNULL, shell=True) == 0

    def sii_read(self, filepath: str = "somanet_cia402.sii", hex_string: bool = False, slaveid: int = 0) -> bool:
        """
        Read SII content from EEPROM.

        Parameters
        ----------
        filepath : str
            Path to file, where content will be written.
        hex_string : bool
            If True, content will be written in Hex String. Default is binary.
        slaveid : int
            Slave ID

        Returns
        -------
        bool
            True, if successfully read.
        """
        option = "-r"
        if hex_string:
            option += "i"

        command = f"sudo eepromtool {self._if} {slaveid + 1} {option} {filepath}"
        return sp.call(command, stdout=sp.DEVNULL, shell=True) == 0

    def write_alias(self, alias: int, slaveid: int = 0) -> bool:
        """
        Write alias to slave.

        Parameters
        ----------
        alias : int
            Desired alias address
        slaveid : int
            Slave ID

        Returns
        -------
        bool
            True, if successfully set.
        """
        command = f"sudo eepromtool {self._if} {slaveid + 1} -walias {alias}"
        return sp.call(command, stdout=sp.DEVNULL, shell=True) == 0

import glob
import logging
import os
import re
import subprocess as sp
import sys
import tempfile
import time
import zipfile
from typing import Union, List, Dict, Type

__all__ = [
    "ExceptionIgH",
    "EtherCATMaster",
]

logger = logging.getLogger(__file__)
logging.basicConfig(format='[%(levelname)s] %(message)s')

if sys.platform != 'linux':
    exit(1)

# start / stop ethercat kernel module (run as root!)
# IgH EtherCAT master must be installed
ecat_master = "/etc/init.d/ethercat"

# ethercat control command
ETHERCAT_PATH = "/opt/etherlab/bin/ethercat"
ETHERCAT_CMDS = ["master", "slaves", "sii_read", "sii_write"]


class ExceptionIgH(Exception):
    pass


if not os.path.isfile(ETHERCAT_PATH):
    logger.warning('EtherCAT Master IgH is not installed.\n'
                   'To install IgH go to "https://github.com/synapticon/Etherlab_EtherCAT_Master/releases".')

SyncManager = {
    "MBoxIn":    0,
    "MBoxOut":   1,
    "BufferIn":  2,
    "BufferOut": 3
}

ECAT_TIMEOUT = 10  # seconds


class EtherCATMaster:
    """
    Base Class to communicate with the IgH EtherCAT Master. This class supports
    start and stop of the kernel modules and accesses low level EtherCAT functions.

    Dependencies:
    - IgH EtherCAT Master (with Synapticon patches)
    - Synapticons siitool
    """

    types_ = (
        "bool",
        "int8", "int16", "int32", "int64",
        "uint8", "uint16", "uint32", "uint64",
        "float", "double",
        "string", "octet_string", "unicode_string",
        "sm8", "sm16", "sm32", "sm64",
    )

    states = (
        "INIT", "PREOP", "BOOT", "SAFEOP", "OP",
    )

    def __init__(self):
        """
        Init Ethercat Module.
        Prints error (No exception on purpose), if IgH is not installed

        """
        if not os.path.isfile(ETHERCAT_PATH):
            logger.error('EtherCAT Master IgH is not installed.\n'
                         'To install IgH go to "https://github.com/synapticon/Etherlab_EtherCAT_Master/releases".')

        self.active = False
        self.siiprint = ""
        self.re_int_value = re.compile(r'(0x\w+ )?(-?\d+)')
        self.re_float_value = re.compile(r'(-?\d+.\d+)')

    def start(self) -> None:
        """
        Starts IgH Ethercat Master
        """
        self.active = sp.call(["sudo", ecat_master, "start"], stdout=sp.DEVNULL)

    def stop(self) -> None:
        """
        Stops IgH Ethercat Master
        """
        if sp.call(["sudo", ecat_master, "stop"], stdout=sp.DEVNULL):
            self.active = False

    def restart(self) -> None:
        """
        Restarts IgH Ethercat Master
        """
        self.stop()
        self.start()

    @staticmethod
    def is_active() -> bool:
        """
        Tests, if the communication is active.

        Returns
        -------
        bool
            True, if communication with slave is possible.
        """

        command = f"sudo {ETHERCAT_PATH} slaves"
        try:
            res_str = sp.check_output(command, shell=True, stderr=sp.STDOUT)
        except sp.CalledProcessError as e:
            res_str = e.output

        return 'Failed' not in res_str.decode()

    def set_state(self, state: str, ignore_timeout: bool = False, slaveid: int = 0) -> bool:
        """
        Set Ethercat state. Possible states are "INIT", "PREOP", "BOOT", "SAFEOP" or "OP".

        Parameters
        ----------
        state : str
            Desired state.
        ignore_timeout : bool
            Ignore timeout. Exit function without verifying, if the state was reached.
        slaveid : int
            Slave ID. First slave = 0.

        Raises
        ------
            ExceptionIgH: If invalid state was requested.
            ExceptionIgH: If not able to set the state.
            ExceptionIgH: If timeout occured.

        Returns
        -------
        bool
            True, if new state was setted.

        """
        _state = state.upper()
        if not _state in self.states:
            raise ExceptionIgH(f"Invalid state {_state}")

        command = f"sudo {ETHERCAT_PATH} state -p {slaveid} {_state}"

        t0 = time.time()
        act_state = None
        while act_state != _state:
            if sp.call(command, stdout=sp.DEVNULL, shell=True) != 0:
                raise ExceptionIgH(f'Set State {_state}')

            act_state = self.get_state(slaveid)
            if time.time() - t0 > ECAT_TIMEOUT:
                raise ExceptionIgH(f'Timeout: Set State {_state}')

            if ignore_timeout:
                return True

        return act_state == _state

    @staticmethod
    def get_state(slaveid: int = 0) -> str:
        """
        Get current state of specific slave.

        Parameters
        ----------
        slaveid : int
            Slave ID

        Returns
        -------
        str
            Current state.

        """
        command = f"sudo {ETHERCAT_PATH} slaves -p {slaveid}"
        state_string = sp.check_output(command,
                                       universal_newlines=True,
                                       shell=True)
        res = re.match(r'\d *\d+:\d+ +(.+?) +. (.+$)', state_string)
        if res:
            state = res.group(1)
            return state.upper()
        return 'None'

    @staticmethod
    def slaves() -> int:
        """
        Return amount of connected slaves.

        Returns
        -------
        int
        """
        command = f"sudo {ETHERCAT_PATH} slaves | wc -l"
        slavecount = sp.check_output(command,
                                     universal_newlines=True,
                                     shell=True)
        return int(slavecount)

    def sii_read(self, slaveid: int = 0) -> str:
        """
        Read SII content from EtherCAT IC. Processed by siitool.

        Parameters
        ----------
        slaveid : int
            Slave ID

        Returns
        -------
        str
            Output from siitool.

        """
        command = f"sudo {ETHERCAT_PATH} sii_read -p {slaveid} | siitool -p"
        self.siiprint = sp.check_output(command, universal_newlines=True, shell=True)

        return self.siiprint

    @staticmethod
    def sii_write(filepath: str = "somanet_cia402.sii", slaveid: int = 0) -> bool:
        """
        Writes SII file to EtherCAT IC.

        Parameters
        ----------
        filepath : str
            Path to SII file.
        slaveid : int
            Slave ID

        Raises
        ------
            ExceptionIgH: If file does not exists.
            ExceptionIgH: If not able to set the alias.

        Returns
        -------
        bool
            True, if successfully written.

        """
        if not os.path.exists(filepath):
            raise ExceptionIgH(f"File '{filepath}' not found.")

        command = f"sudo {ETHERCAT_PATH} alias -f -p {slaveid} 0"

        if sp.call(command, stdout=sp.DEVNULL, shell=True, timeout=20) != 0:
            raise ExceptionIgH("Cannot set alias")

        command = f"sudo {ETHERCAT_PATH} sii_write -f -p {slaveid} {filepath}"

        return sp.call(command, stdout=sp.DEVNULL, shell=True, timeout=60) == 0

    @staticmethod
    def foe_write(filepath: str, filename: str = None, slaveid: int = 0) -> bool:
        """
        Writes file to EtherCAT slave.

        Parameters
        ----------
        filepath : str
            File path.
        filename : str
            Alternative file name on target slave.
        slaveid : int
            Slave ID

        Raises
        ------
            ExceptionIgH: If file not exists.
            ExceptionIgH: If path leads not to a file.

        Returns
        -------
        bool
            True, if successfully written.

        """
        if not os.path.exists(filepath):
            raise ExceptionIgH(f"No valid file path: {filepath}")

        if not os.path.isfile(filepath):
            raise ExceptionIgH(f"Not a valid file: {filepath}")

        command = f"sudo {ETHERCAT_PATH} foe_write -p {slaveid} {filepath}"

        if filename is not None:
            command += f' -o {filename}'

        logger.debug(f"[foe_write] Command: {command}")

        return sp.call(command, stdout=sp.DEVNULL, shell=True) == 0

    @staticmethod
    def foe_read(cmd: str, output: Union[Type[str], Type[bytes]] = None, slaveid: int = 0) -> Union[bool, bytes, str]:
        """
        Reads file from EtherCAT slave.

        Parameters
        ----------
        cmd : str
            Read command or file name.
        output : Union[Type[str], Type[bytes]]
            Output format. Use literal str/bytes objects. If None, returns bool
        slaveid : int
            Slave ID

        Raises
        ------
            ExceptionIgH: If reading file failed
            ExceptionIgH: If output type is unknown.

        Returns
        -------
        Union[bool, bytes, str]
            True, if no output is required and file was successfully read.
            Otherwise output in bytes or str
        """
        command = f"sudo {ETHERCAT_PATH} foe_read -p {slaveid} {cmd}"
        logger.debug(f"[foe_read] Command: {command}")
        if output is not None:
            try:
                f = sp.check_output(command, shell=True)
            except sp.CalledProcessError as e:
                raise ExceptionIgH(e)

            if output is str:
                return f.decode()
            elif output is bytes:
                return f
            else:
                raise ExceptionIgH(f"Unknown output type {output}")
        else:
            return sp.call(command, stdout=sp.DEVNULL, shell=True) == 0

    def flash_fw(self, filepath: str, slaveid: int = 0) -> bool:
        """
        Flash firmware to EtherCAT Slave. Set's automatically state BOOT.

        Parameters
        ----------
        filepath : str
            Path to firmware file. Can be the binary file with pattern "app.*.bin" or a SOMANET package
            (Will only flash the firmware binary).
        slaveid : int
            Slave ID

        Raises
        ------
            ExceptionIgH: If firmware file does not exists
            ExceptionIgH: If firmware is not a valid SOMANET firmware.

        Returns
        -------
        bool
            True, if successfully written.

        """
        if not os.path.exists(filepath):
            raise ExceptionIgH(f'File does not exists')

        file_name = os.path.basename(filepath)

        if re.match(r"^package.+\.zip$", file_name, re.M):
            # Unzip package to a temporary directory.
            dtemp = tempfile.mkdtemp(None, 'EtherCATMaster-')
            with zipfile.ZipFile(filepath) as zf:
                zf.extractall(dtemp)
            filepath = glob.glob(os.path.join(dtemp, '*.bin'))[0]

        elif not re.match(r'^app.+\.bin$', file_name, re.M):
            raise ExceptionIgH(f'{file_name}" is not a valid SOMANET firmware')

        logger.debug("Set BOOT state...")

        self.set_state("BOOT")

        time.sleep(0.1)
        logger.debug("Flash firmware...")

        return self.foe_write(slaveid=slaveid, filepath=filepath)

    def upload(self, index: int, subindex: int, type: str = None, error: bool = False, slaveid: int = 0) -> Union[int, float, str]:
        """
        Reads object from object dictionary.
        Converts int or float objects to corresponding types.

        Parameters
        ----------
        index : int
            Dictionary index
        subindex : int
            Dictionary subindex
        type : str
            Dictionary data type.
        error : bool
            If True, then show error message during upload.
        slaveid : int
            Slave ID

        Raises
        ------
            ExceptionIgH: If data type is invalid.

        Returns
        -------
        Union[int, float, str]
            Integer, floating point or string object.

        """
        _type = ""
        if isinstance(type, str):
            if type not in self.types_:
                raise ExceptionIgH(f"Type '{type}' is not valid. These are valid types: {self.types_}")

            _type = f"--type {type}"

        command = f"sudo {ETHERCAT_PATH} upload -p {slaveid} 0x{index:x} {subindex} {_type}"

        if error:
            _err = sp.STDOUT
        else:
            _err = sp.DEVNULL

        output = sp.check_output(command, shell=True, stderr=_err)

        # Try to decode the output. If not possible return the output directly. Then it's no string.
        try:
            output = output.decode().strip()
        except UnicodeDecodeError:
            return output

        # Check if output is a integer.
        res = self.re_int_value.match(output)
        if res:
            # return Int value
            return int(res.group(2))

        # Check if output is a float.
        res = self.re_float_value.match(output)
        if res:
            return float(res.group(1))

        # Return string.
        return output

    def download(self, index: int, subindex: int, value: Union[str, int, float], type: str = None, slaveid: int = 0) -> bool:
        """
        Write new value to object dictionary.

        Parameters
        ----------
        index : int
            Dictionary index
        subindex : int
            Dictionary subindex
        value : Union[str, int, float]
            New value.
        type : str
            Dictionary data type.
        slaveid : int
            Slave ID

        Raises
        ------
            ExceptionIgH: If data type is invalid.

        Returns
        -------
        bool
            True, if successfully written.

        """
        _type = ""
        if isinstance(type, str):
            if type not in self.types_:
                raise ExceptionIgH(f"Type '{type}' is not valid. These are valid types: {self.types_}")

            _type = f"--type {type}"

        command = f"sudo {ETHERCAT_PATH} download -p {slaveid} 0x{index:x} {subindex} {value} {_type}"

        return sp.call(command, stdout=sp.DEVNULL, shell=True) == 0

    def get_bootloader_version(self, slaveid: int = 0) -> str:
        """
        Returns the bootloader version. Sets automatically the BOOT state.

        Parameters
        ----------
        slaveid : int
            Slave ID

        Returns
        -------
        str
            Bootloader version as string.
        """

        self.set_state("BOOT", slaveid=slaveid)
        return self.foe_read(cmd="bversion", slaveid=slaveid, output=str).strip()

    def get_bootloader_help(self, slaveid: int = 0) -> str:
        """
        Returns the bootloader help text. Sets automatically the BOOT state.

        Parameters
        ----------
        slaveid : int
            Slave ID

        Returns
        -------
        str
            Bootloader help text.
        """

        self.set_state("BOOT", slaveid=slaveid)
        return self.foe_read(cmd="help", slaveid=slaveid, output=str).strip()

    def ls(self, slaveid: int = 0) -> List[Dict[str, Union[str, int]]]:
        """
        Returns the bootloader version. Sets automatically the BOOT state.

        Parameters
        ----------
        slaveid : int
            Slave ID

        Returns
        -------
        List[Dict[str, Union[str, int]]]
            List with dictionary with items name:str and size:int in bytes.
        """
        res = list()
        _list = self.foe_read(cmd="fs-getlist", slaveid=slaveid, output=str).strip()
        file_list = re.findall(r'(.+), size: (.+)', _list)

        for name, size in file_list:
            res.append({"name": name, "size": int(size)})

        return res

    def rm(self, filename: str, slaveid: int = 0) -> str:
        """
        Removes file from file system.

        Parameters
        ----------
        filename: str
            Name of file, which will be removed.
        slaveid : int
            Slave ID

        Returns
        -------
        str
            Response message.
        """

        return self.foe_read(cmd=f"fs-remove={filename}", slaveid=slaveid, output=str).strip()

    def filesystem_unlock(self, password: str, slaveid: int = 0) -> str:
        """
        Unlocks the file protection. Necessary when deleting hidden files (.filename).

        Parameters
        ----------
        password: str
            Password to unlock the protection.
        slaveid : int
            Slave ID

        Returns
        -------
        str
            Response message.
        """

        return self.foe_read(cmd=f"fs-stackunlock={password}", slaveid=slaveid, output=str).strip()

    def get_filesystem_info(self, slaveid: int = 0) -> Dict[str, int]:
        """
        Returns total, used and free memory on filesystem in bytes.

        Parameters
        ----------
        slaveid : int
            Slave ID

        Raises
        ------
            ExceptionIgH: If not possible, to parse filesystem info message.

        Returns
        -------
        Dict[str, int]
            Dict with total and used amount of bytes.
        """
        info = self.foe_read(cmd=f"fs-info", slaveid=slaveid, output=str).strip()
        res = re.findall(r'(\d+)', info)
        if not res:
            raise ExceptionIgH("Could not parse filesystem info message")

        return {"total": int(res[0]), "used": int(res[1]), "free": int(res[0]) - int(res[1])}

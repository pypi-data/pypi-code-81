import json
import logging
import time
from typing import Union, List, Tuple

from .dataformat import *
from ..communication.ethercat.EtherCATMaster import EtherCATMaster

logger = logging.getLogger(__file__)
logging.basicConfig(format='[%(levelname)s] %(message)s')


##################### DEPRECATED #######################

class JSONInfo:
    file_name = 'stack_info.json'

    def __init__(self, mac: str = '', stack_serial: str = '', *boards: Tuple[str]):
        """
        Create new JSONInfo object
        Parameters
        ----------
        mac : str
            Mac address
        stack_serial : str
            Serial number of stack/servo drive.
        boards : List[Tuple[str]]
            List with board information.
        """
        self.mac = mac
        self.stack_serial = stack_serial
        self.board_list = boards
        self.ecat = EtherCATMaster()

    def generate(self, fs_unlock_pw: str = None, postfix: str = None) -> bool:
        """
        Generate Stack Info file.

        Parameters
        ----------
        fs_unlock_pw : str
            Password to unlock filesystem. If set, file will be flashed via EtherCAT to a servo drive.
        postfix : str
            Optional postfix for file name. (e.g. timestamp)

        Returns
        -------
        bool
            True if successfully generated and flashed.
        """

        # Create a new stack
        stack = StackInfo()
        # Take the MAC address from the input arguments
        if self.mac != '':
            self.mac = self.mac.replace(':', '')
            self.mac = self.mac.replace('-', '')
            stack.set_mac_address(int(self.mac, 16))
        # Add the stack serial number
        if self.stack_serial != '':
            stack.set_stack_serial_number(self.stack_serial)

        # Collect all the board infos and add them to the stack
        try:
            for arg_board in self.board_list:
                board = BoardInfo()
                board.set_description(arg_board[0])
                board.set_revision(arg_board[1])
                board.set_serial_number(arg_board[2])
                stack.add_board_info(board)
        except ValueError as e:
            logger.error(e)
            return False

        # Log the results of the stack_info file.
        lines = str(stack).split('\n')
        for line in lines:
            logger.info(line)

        logger.info(json.dumps(stack, ensure_ascii=False, default=lambda o: o.__dict__))

        if postfix:
            self.file_name += '_' + postfix

        # Write to a file
        with open(self.file_name, 'w') as stack_info_file:
            json_file = json.dumps(stack, ensure_ascii=False, default=lambda o: o.__dict__)
            stack_info_file.write(json_file)

        # Flash the stack_info.json file to the flash memory of the Core board.
        if fs_unlock_pw is not None:
            # Write this to flash using a private bootloader method
            try:
                if not self.ecat.is_active():
                    self.ecat.start()
                    time.sleep(2)
                if not self.ecat.set_state('BOOT'):
                    raise Exception('Set slave to state BOOT failed')
                time.sleep(0.1)
                if not self.ecat.filesystem_unlock(fs_unlock_pw):
                    raise Exception('Unlock stack failed')
                time.sleep(0.1)
                if not self.ecat.foe_write(filepath=self.file_name):
                    raise Exception('Writing file failed')
                time.sleep(0.1)
                read_json = self.ecat.foe_read(self.file_name, output=str)
                if read_json != json_file:
                    raise Exception('Files doesn\'t match')
            except Exception as e:
                logger.error(e)
                logger.error("The file was not successfully flashed to the stack.")
                return False
        else:
            logger.warning("The file was created but not flashed to the board. Remove the --skip_flash argument if you want that.")
        return True


##################### END DEPRECATED #######################


class BuildHardwareDescription:
    file_name = '.hardware_description'

    def __init__(self):
        self.device: DeviceInfo
        self.assembly: AssemblyInfo
        self.json_content: str
        self.ecat: EtherCATMaster = EtherCATMaster()

    def __generate_component(self, component: List[str]) -> ComponentInfo:
        """
        Create a new Component Info object and add information to it.

        Parameters
        ----------
        component : List[str]
            Tuple/list with component information.

        Returns
        -------
        ComponentInfo
            New ComponentInfo object
        """

        comp = ComponentInfo()
        comp.set_name(component[0])
        comp.set_version(component[1])
        comp.set_serial_number(component[2])
        return comp

    def __set_info(self, type: Union[DeviceInfo, AssemblyInfo], name: str, id: Union[int, str], version: Union[int, str], sn: str, components: List[List[str]]):
        """
        Set new Device or assembly info.

        Parameters
        ----------
        type : Union[DeviceInfo, AssemblyInfo]
            New Device or Assembly object
        name : str
            Assembly name
        id : str
            ID
        version : str
            Version
        sn : str
            serial number
        components : List[List[str]]
            List of components
        """
        type.set_name(name)
        type.set_id(id)
        type.set_version(version)
        type.set_serial_number(sn)
        if components:
            for c in components:
                type.add_component(self.__generate_component(c))

    def set_device(self, name: str, id: Union[int, str], version: Union[int, str], sn: str, components: List[List[str]], mac: Union[int, str] = None) -> bool:
        """
        Set Device info.

        Parameters
        ----------
        name : str
            Assembly name
        id : str
            ID
        version : str
            Version
        sn : str
            serial number
        components : List[List[str]]
            List of components
        mac : str
            MAC Address

        Returns
        -------
        bool
            True if successfully created.

        """
        try:
            self.device = DeviceInfo()
            if mac:
                self.device.set_mac_address(mac)
            self.__set_info(self.device, name, id, version, sn, components)
        except ExceptionHardwareDescription as e:
            logger.error(e)
            return False
        return True

    def set_assembly(self, name: str, id: Union[int, str], version: Union[int, str], sn: str, components: List[List[str]] = None) -> bool:
        """
        Set assembly info.

        Parameters
        ----------
        name : str
            Assembly name
        id : str
            ID
        version : str
            Version
        sn : str
            serial number
        components : List[List[str]]
            List of components

        Returns
        -------
        bool
            True, if successfully created.

        """
        try:
            self.assembly = AssemblyInfo()
            self.__set_info(self.assembly, name, id, version, sn, components)
        except ExceptionHardwareDescription as e:
            logger.error(e)
            return False
        return True

    def generate(self, postfix: str = None, write_file: bool = True) -> Union[str, None]:
        """
        Generate new file.

        Parameters
        ----------
        postfix : str
            Optional postfix, concat to file name (e.g. timestamp)
        write_file : bool
            If true, create a JSON file with name .hardware_description_<postfix>.

        Returns
        -------
        Union[str, None]
            JSON file content, if write_file is False, otherwise None.

        """
        # Create a new stack
        hw = HardwareDescription()
        hw.set_device(self.device)
        if hasattr(self, "assembly"):
            hw.set_assembly(self.assembly)

        # Log the results of the stack_info file.
        lines = str(hw).split('\n')

        for line in lines:
            logger.info(line)

        logger.info(hw)
        self.json_content = json.dumps(hw, ensure_ascii=False, default=lambda o: o.__dict__)
        logger.info(self.json_content)

        if not write_file:
            return self.json_content

        if postfix:
            self.file_name += '_' + postfix
        # Write to a file
        with open(self.file_name, 'w') as hardware_description_file:
            hardware_description_file.write(self.json_content)

        return None

    def flash(self, fs_unlock_password: str) -> bool:
        """
        Flash JSON file to servo drive.
        Parameters
        ----------
        fs_unlock_password : str
            Password to unlock filesystem protection.

        Returns
        -------
        bool
            True, if successfully written.

        """
        # Write this to flash using a private bootloader method
        try:
            if not self.ecat.is_active():
                self.ecat.start()
                time.sleep(2)

            if not self.ecat.set_state('BOOT'):
                raise ExceptionHardwareDescription('Set slave to state BOOT failed')

            time.sleep(0.1)

            if not self.ecat.filesystem_unlock(fs_unlock_password):
                raise ExceptionHardwareDescription('Unlock stack failed')

            time.sleep(0.1)

            if not self.ecat.foe_write(filepath=self.file_name):
                raise ExceptionHardwareDescription('Writing file failed')

            time.sleep(0.1)

            read_json = self.ecat.foe_read(self.file_name, output=str)
            if read_json != self.json_content:
                logger.error(read_json)
                logger.error(self.json_content)
                raise ExceptionHardwareDescription('Files doesn\'t match')

        except ExceptionHardwareDescription as e:
            logger.error(e)
            logger.error("The file was not successfully flashed to the stack.")
            return False
        return True

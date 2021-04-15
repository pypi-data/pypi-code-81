from .constants import *
from .structures import *
import ctypes
from ctypes.wintypes import DWORD
from ctypes.wintypes import BOOL
from ctypes.wintypes import HWND
from ctypes.wintypes import PDWORD
from ctypes.wintypes import LPVOID
from ctypes.wintypes import HKEY
from ctypes.wintypes import LPCWSTR
from ctypes.wintypes import LPDWORD

setupapi = ctypes.windll.LoadLibrary("setupapi")
advapi32 = ctypes.windll.LoadLibrary("Advapi32")


# error check
def error_check(result, func, args):
    if not result:
        raise ctypes.WinError()
    return result


class Port:
    def __init__(self, num, name, hwid):
        self.num = num
        self.name = name
        self.hwid = hwid

    def __repr__(self):
        return "Port({}, {}, {})".format(self.num, self.name, self.hwid)

    def __getitem__(self, item):
        if isinstance(item, str) and hasattr(self, item):
            return getattr(self, item)
        elif isinstance(item, int):
            if item == 0:
                return self.num
            elif item == 1:
                return self.name
            elif item == 2:
                return self.hwid
            else:
                raise IndexError("Port only support indexing 0, 1, 2")
        else:
            raise TypeError("Fail to get property from Port.")


# functions
RegQueryValueExW = advapi32.RegQueryValueExW
RegQueryValueExW.argtypes = [HKEY, LPCWSTR, LPDWORD, LPDWORD, LPBYTE, LPDWORD]
RegQueryValueExW.restype = ctypes.wintypes.LONG

RegCloseKey = advapi32.RegCloseKey
RegCloseKey.argtypes = [HKEY]
RegCloseKey.restype = DWORD

SetupDiClassGuidsFromNameW = setupapi.SetupDiClassGuidsFromNameW
SetupDiClassGuidsFromNameW.argtypes = [PCWSTR, ctypes.POINTER(GUID), DWORD, PDWORD]
SetupDiClassGuidsFromNameW.restype = BOOL
SetupDiClassGuidsFromNameW.errcheck = error_check

SetupDiGetClassDevsW = setupapi.SetupDiGetClassDevsW
SetupDiGetClassDevsW.argtypes = [ctypes.POINTER(GUID), PCWSTR, HWND, DWORD]
SetupDiGetClassDevsW.restype = HWND
SetupDiGetClassDevsW.errcheck = error_check

SetupDiEnumDeviceInfo = setupapi.SetupDiEnumDeviceInfo
SetupDiEnumDeviceInfo.argtypes = [LPVOID, DWORD, ctypes.POINTER(SP_DEVINFO_DATA)]
SetupDiEnumDeviceInfo.restype = BOOL

SetupDiOpenDevRegKey = setupapi.SetupDiOpenDevRegKey
SetupDiOpenDevRegKey.argtypes = [LPVOID, ctypes.POINTER(SP_DEVINFO_DATA), DWORD, DWORD, DWORD, DWORD]
SetupDiOpenDevRegKey.restype = HKEY
SetupDiOpenDevRegKey.errcheck = error_check

SetupDiGetDeviceRegistryPropertyW = setupapi.SetupDiGetDeviceRegistryPropertyW
SetupDiGetDeviceRegistryPropertyW.argtypes = [LPVOID, ctypes.POINTER(SP_DEVINFO_DATA), DWORD, PDWORD, PBYTE, DWORD, PDWORD]
SetupDiGetDeviceRegistryPropertyW.restype = BOOL

SetupDiDestroyDeviceInfoList = setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.argtypes = [LPVOID]
SetupDiDestroyDeviceInfoList.restype = BOOL

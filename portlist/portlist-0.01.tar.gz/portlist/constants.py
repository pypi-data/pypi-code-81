# Definition of args
import ctypes


PBYTE = LPBYTE = ctypes.c_void_p
PCWSTR = ctypes.c_wchar_p
DIGCF_PRESENT = 0x00000002  # SetupDiGetClassDevsW param
DICS_FLAG_GLOBAL = 0x00000001  # SetupDiOpenDevRegKey
DIREG_DEV = 0x00000001  # SetupDiOpenDevRegKey
SPDRP_LOCATION_PATHS = 0x00000023  # SetupDiGetDeviceRegistryPropertyW
SPDRP_FRIENDLYNAME = 0x0000000C  # SetupDiGetDeviceRegistryPropertyW
SPDRP_HARDWAREID = 0x00000001  # SetupDiGetDeviceRegistryPropertyW

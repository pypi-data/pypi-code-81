from portlist import *
import ctypes


def get_port():
    # Get Ports GUIDs
    ports_GUIDs = (GUID * 8)()
    ports_required_size = DWORD()
    SetupDiClassGuidsFromNameW(
        'Ports',
        ports_GUIDs,
        ctypes.sizeof(ports_GUIDs),
        ctypes.byref(ports_required_size)
    )

    # Get Modem GUIDs
    modem_GUIDs = (GUID * 8)()
    modem_required_size = DWORD()
    SetupDiClassGuidsFromNameW(
        'Modem',
        modem_GUIDs,
        ctypes.sizeof(modem_GUIDs),
        ctypes.pointer(modem_required_size)
    )

    # Modem GUIDs and Ports GUIDS
    GUIDs = ports_GUIDs[:ports_required_size.value] + modem_GUIDs[:modem_required_size.value]

    for guid in GUIDs:
        gid = SetupDiGetClassDevsW(
                ctypes.pointer(guid),
                None,
                None,
                DIGCF_PRESENT
        )
        dev_info = SP_DEVINFO_DATA()
        dev_info.cbSize = ctypes.sizeof(dev_info)

        index = 0
        while SetupDiEnumDeviceInfo(gid, index, ctypes.pointer(dev_info)):
            index += 1

            hkey = SetupDiOpenDevRegKey(
                gid,
                ctypes.pointer(dev_info),
                DICS_FLAG_GLOBAL,
                0,
                DIREG_DEV,
                0x00000001
            )

            port_name_buffer = ctypes.create_unicode_buffer(250)
            RegQueryValueExW(
                hkey,
                "PortName",
                None,
                None,
                ctypes.byref(port_name_buffer),
                ctypes.c_ulong(ctypes.sizeof(port_name_buffer) - 1)
            )
            RegCloseKey(hkey)

            friendly_name_buffer = ctypes.create_unicode_buffer(250)
            SetupDiGetDeviceRegistryPropertyW(
                gid,
                ctypes.pointer(dev_info),
                SPDRP_FRIENDLYNAME,
                None,
                ctypes.pointer(friendly_name_buffer),
                ctypes.sizeof(friendly_name_buffer) - 1,
                None,
            )

            hardware_id_buffer = ctypes.create_unicode_buffer(250)
            SetupDiGetDeviceRegistryPropertyW(
                gid,
                ctypes.pointer(dev_info),
                SPDRP_HARDWAREID,
                None,
                ctypes.pointer(hardware_id_buffer),
                ctypes.sizeof(hardware_id_buffer) - 1,
                None,
            )
            yield Port(port_name_buffer.value, friendly_name_buffer.value, hardware_id_buffer.value)
        SetupDiDestroyDeviceInfoList(gid)


def ports():
    return list(get_port())


if __name__ == '__main__':
    ports = ports()
    for port in ports:
        print(port.num)

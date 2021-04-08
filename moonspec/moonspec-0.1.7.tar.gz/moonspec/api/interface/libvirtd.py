import logging
from os import putenv
from typing import Optional, Any

putenv('LIBVIRT_AUTOSTART', '0')  # Doh...

LOGGER = logging.getLogger('moonspec')

has_libvirt: bool = False
try:
    import libvirt  # type: ignore
    from libvirt import virConnect

    has_libvirt = True
except ImportError:
    libvirt = None
    virConnect = None
    has_libvirt = False


class LibvirtApi:
    _connection_ref: Optional[Any] = None
    _connection_ref_ro: Optional[Any] = None

    @staticmethod
    def _connection() -> virConnect:
        if not has_libvirt:
            raise RuntimeError('Libvirt is not supported')

        if LibvirtApi._connection_ref is not None:
            return LibvirtApi._connection_ref

        try:
            connection = libvirt.open(None)
        except libvirt.libvirtError as e:
            LOGGER.error('Failed to connect to libvirt', exc_info=e)
            raise RuntimeError('Libvirt is not supported')

        LibvirtApi._connection_ref = connection
        return connection

    @staticmethod
    def _connection_ro() -> virConnect:
        if not has_libvirt:
            raise RuntimeError('Libvirt is not supported')

        if LibvirtApi._connection_ref_ro is not None:
            return LibvirtApi._connection_ref_ro

        try:
            connection = libvirt.openReadOnly(None)
        except libvirt.libvirtError as e:
            LOGGER.error('Failed to connect to libvirt', exc_info=e)
            raise RuntimeError('Libvirt is not supported')

        LibvirtApi._connection_ref_ro = connection

        return connection

    @staticmethod
    def ro() -> virConnect:
        return LibvirtApi._connection_ro()

    @staticmethod
    def admin() -> virConnect:
        return LibvirtApi._connection()

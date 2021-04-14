'''_1946.py

BearingInnerSocket
'''


from mastapy.system_model.connections_and_sockets import _1962
from mastapy._internal.python_net import python_net_import

_BEARING_INNER_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BearingInnerSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingInnerSocket',)


class BearingInnerSocket(_1962.MountableComponentInnerSocket):
    '''BearingInnerSocket

    This is a mastapy class.
    '''

    TYPE = _BEARING_INNER_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingInnerSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

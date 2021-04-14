'''_1220.py

CycloidalDiscMaterialDatabase
'''


from mastapy.materials import _236
from mastapy.cycloidal import _1219
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Cycloidal', 'CycloidalDiscMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscMaterialDatabase',)


class CycloidalDiscMaterialDatabase(_236.MaterialDatabase['_1219.CycloidalDiscMaterial']):
    '''CycloidalDiscMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

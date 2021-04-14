'''_2165.py

ActiveImportedFESelection
'''


from mastapy.system_model.part_model.configurations import _2172
from mastapy.system_model.part_model import _2020
from mastapy.system_model.imported_fes import _1954
from mastapy._internal.python_net import python_net_import

_ACTIVE_IMPORTED_FE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveImportedFESelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveImportedFESelection',)


class ActiveImportedFESelection(_2172.PartDetailSelection['_2020.ImportedFEComponent', '_1954.ImportedFE']):
    '''ActiveImportedFESelection

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_IMPORTED_FE_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveImportedFESelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

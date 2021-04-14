'''_2281.py

ActiveFESubstructureSelection
'''


from mastapy.system_model.part_model.configurations import _2288
from mastapy.system_model.part_model import _2125
from mastapy.system_model.fe import _2057
from mastapy._internal.python_net import python_net_import

_ACTIVE_FE_SUBSTRUCTURE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveFESubstructureSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveFESubstructureSelection',)


class ActiveFESubstructureSelection(_2288.PartDetailSelection['_2125.FEPart', '_2057.FESubstructure']):
    '''ActiveFESubstructureSelection

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_FE_SUBSTRUCTURE_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveFESubstructureSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

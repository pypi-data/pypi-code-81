'''_2286.py

ActiveFESubstructureSelection
'''


from mastapy.system_model.part_model.configurations import _2293
from mastapy.system_model.part_model import _2130
from mastapy.system_model.fe import _2062
from mastapy._internal.python_net import python_net_import

_ACTIVE_FE_SUBSTRUCTURE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveFESubstructureSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveFESubstructureSelection',)


class ActiveFESubstructureSelection(_2293.PartDetailSelection['_2130.FEPart', '_2062.FESubstructure']):
    '''ActiveFESubstructureSelection

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_FE_SUBSTRUCTURE_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveFESubstructureSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

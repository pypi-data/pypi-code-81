'''_2067.py

FESubstructureWithSelection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.fe import (
    _2062, _2055, _2078, _2040
)
from mastapy._internal.python_net import python_net_import

_FE_SUBSTRUCTURE_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructureWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('FESubstructureWithSelection',)


class FESubstructureWithSelection(_2040.BaseFEWithSelection):
    '''FESubstructureWithSelection

    This is a mastapy class.
    '''

    TYPE = _FE_SUBSTRUCTURE_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FESubstructureWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def selected_nodes(self) -> 'str':
        '''str: 'SelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectedNodes

    @property
    def fe_substructure(self) -> '_2062.FESubstructure':
        '''FESubstructure: 'FESubstructure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2062.FESubstructure)(self.wrapped.FESubstructure) if self.wrapped.FESubstructure else None

    @property
    def element_face_groups(self) -> 'List[_2055.ElementFaceGroupWithSelection]':
        '''List[ElementFaceGroupWithSelection]: 'ElementFaceGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ElementFaceGroups, constructor.new(_2055.ElementFaceGroupWithSelection))
        return value

    @property
    def node_groups(self) -> 'List[_2078.NodeGroupWithSelection]':
        '''List[NodeGroupWithSelection]: 'NodeGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.NodeGroups, constructor.new(_2078.NodeGroupWithSelection))
        return value

    def create_element_face_group(self):
        ''' 'CreateElementFaceGroup' is the original name of this method.'''

        self.wrapped.CreateElementFaceGroup()

    def ground_selected_faces(self):
        ''' 'GroundSelectedFaces' is the original name of this method.'''

        self.wrapped.GroundSelectedFaces()

    def remove_grounding_on_selected_faces(self):
        ''' 'RemoveGroundingOnSelectedFaces' is the original name of this method.'''

        self.wrapped.RemoveGroundingOnSelectedFaces()

    def create_condensation_node_connected_to_current_selection(self):
        ''' 'CreateCondensationNodeConnectedToCurrentSelection' is the original name of this method.'''

        self.wrapped.CreateCondensationNodeConnectedToCurrentSelection()

    def create_node_group(self):
        ''' 'CreateNodeGroup' is the original name of this method.'''

        self.wrapped.CreateNodeGroup()

'''_6522.py

FaceGearSetLoadCase
'''


from typing import List

from mastapy.system_model.part_model.gears import _2204
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6520, _6521, _6531
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'FaceGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetLoadCase',)


class FaceGearSetLoadCase(_6531.GearSetLoadCase):
    '''FaceGearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2204.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2204.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def gears(self) -> 'List[_6520.FaceGearLoadCase]':
        '''List[FaceGearLoadCase]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_6520.FaceGearLoadCase))
        return value

    @property
    def face_gears_load_case(self) -> 'List[_6520.FaceGearLoadCase]':
        '''List[FaceGearLoadCase]: 'FaceGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsLoadCase, constructor.new(_6520.FaceGearLoadCase))
        return value

    @property
    def face_meshes_load_case(self) -> 'List[_6521.FaceGearMeshLoadCase]':
        '''List[FaceGearMeshLoadCase]: 'FaceMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesLoadCase, constructor.new(_6521.FaceGearMeshLoadCase))
        return value

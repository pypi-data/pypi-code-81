'''_4290.py

FaceGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2204
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6522
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4289, _4288, _4295
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'FaceGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetModalAnalysisAtAStiffness',)


class FaceGearSetModalAnalysisAtAStiffness(_4295.GearSetModalAnalysisAtAStiffness):
    '''FaceGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetModalAnalysisAtAStiffness.TYPE'):
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
    def assembly_load_case(self) -> '_6522.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6522.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4289.FaceGearModalAnalysisAtAStiffness]':
        '''List[FaceGearModalAnalysisAtAStiffness]: 'FaceGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsModalAnalysisAtAStiffness, constructor.new(_4289.FaceGearModalAnalysisAtAStiffness))
        return value

    @property
    def face_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4288.FaceGearMeshModalAnalysisAtAStiffness]':
        '''List[FaceGearMeshModalAnalysisAtAStiffness]: 'FaceMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesModalAnalysisAtAStiffness, constructor.new(_4288.FaceGearMeshModalAnalysisAtAStiffness))
        return value

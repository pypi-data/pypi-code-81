'''_4567.py

KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2216
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6558
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4566, _4565, _4561
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed',)


class KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed(_4561.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2216.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2216.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6558.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6558.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_modal_analysis_at_a_speed(self) -> 'List[_4566.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearsModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsModalAnalysisAtASpeed, constructor.new(_4566.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_modal_analysis_at_a_speed(self) -> 'List[_4565.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelMeshesModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesModalAnalysisAtASpeed, constructor.new(_4565.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed))
        return value

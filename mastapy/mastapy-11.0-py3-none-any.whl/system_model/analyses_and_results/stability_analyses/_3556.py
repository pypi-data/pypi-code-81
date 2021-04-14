'''_3556.py

WormGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2227
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6625
from mastapy.system_model.analyses_and_results.stability_analyses import _3557, _3555, _3489
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'WormGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetStabilityAnalysis',)


class WormGearSetStabilityAnalysis(_3489.GearSetStabilityAnalysis):
    '''WormGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2227.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2227.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6625.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6625.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def worm_gears_stability_analysis(self) -> 'List[_3557.WormGearStabilityAnalysis]':
        '''List[WormGearStabilityAnalysis]: 'WormGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsStabilityAnalysis, constructor.new(_3557.WormGearStabilityAnalysis))
        return value

    @property
    def worm_meshes_stability_analysis(self) -> 'List[_3555.WormGearMeshStabilityAnalysis]':
        '''List[WormGearMeshStabilityAnalysis]: 'WormMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesStabilityAnalysis, constructor.new(_3555.WormGearMeshStabilityAnalysis))
        return value

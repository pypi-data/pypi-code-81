'''_3478.py

CylindricalGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2201, _2217
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6500, _6571
from mastapy.system_model.analyses_and_results.stability_analyses import _3479, _3477, _3489
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'CylindricalGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetStabilityAnalysis',)


class CylindricalGearSetStabilityAnalysis(_3489.GearSetStabilityAnalysis):
    '''CylindricalGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2201.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2201.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6500.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6500.CylindricalGearSetLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to CylindricalGearSetLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def cylindrical_gears_stability_analysis(self) -> 'List[_3479.CylindricalGearStabilityAnalysis]':
        '''List[CylindricalGearStabilityAnalysis]: 'CylindricalGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsStabilityAnalysis, constructor.new(_3479.CylindricalGearStabilityAnalysis))
        return value

    @property
    def cylindrical_meshes_stability_analysis(self) -> 'List[_3477.CylindricalGearMeshStabilityAnalysis]':
        '''List[CylindricalGearMeshStabilityAnalysis]: 'CylindricalMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesStabilityAnalysis, constructor.new(_3477.CylindricalGearMeshStabilityAnalysis))
        return value

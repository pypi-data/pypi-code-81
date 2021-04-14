'''_5747.py

WormGearSetHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2227
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6625
from mastapy.system_model.analyses_and_results.system_deflections import _2503
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5745, _5746, _5671
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'WormGearSetHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetHarmonicAnalysis',)


class WormGearSetHarmonicAnalysis(_5671.GearSetHarmonicAnalysis):
    '''WormGearSetHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetHarmonicAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2503.WormGearSetSystemDeflection':
        '''WormGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2503.WormGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_harmonic_analysis(self) -> 'List[_5745.WormGearHarmonicAnalysis]':
        '''List[WormGearHarmonicAnalysis]: 'GearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsHarmonicAnalysis, constructor.new(_5745.WormGearHarmonicAnalysis))
        return value

    @property
    def worm_gears_harmonic_analysis(self) -> 'List[_5745.WormGearHarmonicAnalysis]':
        '''List[WormGearHarmonicAnalysis]: 'WormGearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsHarmonicAnalysis, constructor.new(_5745.WormGearHarmonicAnalysis))
        return value

    @property
    def meshes_harmonic_analysis(self) -> 'List[_5746.WormGearMeshHarmonicAnalysis]':
        '''List[WormGearMeshHarmonicAnalysis]: 'MeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesHarmonicAnalysis, constructor.new(_5746.WormGearMeshHarmonicAnalysis))
        return value

    @property
    def worm_meshes_harmonic_analysis(self) -> 'List[_5746.WormGearMeshHarmonicAnalysis]':
        '''List[WormGearMeshHarmonicAnalysis]: 'WormMeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesHarmonicAnalysis, constructor.new(_5746.WormGearMeshHarmonicAnalysis))
        return value

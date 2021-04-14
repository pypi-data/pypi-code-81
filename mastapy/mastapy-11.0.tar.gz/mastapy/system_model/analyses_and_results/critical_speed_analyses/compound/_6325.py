'''_6325.py

BevelDifferentialGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2191
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6323, _6324, _6330
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6194
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'BevelDifferentialGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundCriticalSpeedAnalysis',)


class BevelDifferentialGearSetCompoundCriticalSpeedAnalysis(_6330.BevelGearSetCompoundCriticalSpeedAnalysis):
    '''BevelDifferentialGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2191.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2191.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2191.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2191.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_critical_speed_analysis(self) -> 'List[_6323.BevelDifferentialGearCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearCompoundCriticalSpeedAnalysis]: 'BevelDifferentialGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundCriticalSpeedAnalysis, constructor.new(_6323.BevelDifferentialGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_meshes_compound_critical_speed_analysis(self) -> 'List[_6324.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis]: 'BevelDifferentialMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6324.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6194.BevelDifferentialGearSetCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6194.BevelDifferentialGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6194.BevelDifferentialGearSetCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6194.BevelDifferentialGearSetCriticalSpeedAnalysis))
        return value

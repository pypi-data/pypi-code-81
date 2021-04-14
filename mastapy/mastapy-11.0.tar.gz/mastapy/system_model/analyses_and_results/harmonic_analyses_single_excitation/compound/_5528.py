'''_5528.py

HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2210
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5526, _5527, _5470
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5399
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation',)


class HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation(_5470.AGMAGleasonConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation):
    '''HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2210.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2210.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2210.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2210.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5526.HypoidGearCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[HypoidGearCompoundHarmonicAnalysisOfSingleExcitation]: 'HypoidGearsCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5526.HypoidGearCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def hypoid_meshes_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5527.HypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[HypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation]: 'HypoidMeshesCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5527.HypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5399.HypoidGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[HypoidGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5399.HypoidGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5399.HypoidGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[HypoidGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5399.HypoidGearSetHarmonicAnalysisOfSingleExcitation))
        return value

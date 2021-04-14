'''_5786.py

BearingCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2118
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5602
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5814
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'BearingCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundHarmonicAnalysis',)


class BearingCompoundHarmonicAnalysis(_5814.ConnectorCompoundHarmonicAnalysis):
    '''BearingCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2118.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2118.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5602.BearingHarmonicAnalysis]':
        '''List[BearingHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5602.BearingHarmonicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundHarmonicAnalysis]':
        '''List[BearingCompoundHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5602.BearingHarmonicAnalysis]':
        '''List[BearingHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5602.BearingHarmonicAnalysis))
        return value

'''_5866.py

PulleyCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2265, _2262
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5707
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5817
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'PulleyCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundHarmonicAnalysis',)


class PulleyCompoundHarmonicAnalysis(_5817.CouplingHalfCompoundHarmonicAnalysis):
    '''PulleyCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2265.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2265.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5707.PulleyHarmonicAnalysis]':
        '''List[PulleyHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5707.PulleyHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5707.PulleyHarmonicAnalysis]':
        '''List[PulleyHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5707.PulleyHarmonicAnalysis))
        return value

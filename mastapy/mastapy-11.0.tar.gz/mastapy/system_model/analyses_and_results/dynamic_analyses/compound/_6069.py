'''_6069.py

ClutchHalfCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2254
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5939
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6085
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ClutchHalfCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundDynamicAnalysis',)


class ClutchHalfCompoundDynamicAnalysis(_6085.CouplingHalfCompoundDynamicAnalysis):
    '''ClutchHalfCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2254.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2254.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5939.ClutchHalfDynamicAnalysis]':
        '''List[ClutchHalfDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5939.ClutchHalfDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5939.ClutchHalfDynamicAnalysis]':
        '''List[ClutchHalfDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5939.ClutchHalfDynamicAnalysis))
        return value

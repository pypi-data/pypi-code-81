'''_6054.py

BearingCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2118
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5924
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6082
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'BearingCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundDynamicAnalysis',)


class BearingCompoundDynamicAnalysis(_6082.ConnectorCompoundDynamicAnalysis):
    '''BearingCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundDynamicAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_5924.BearingDynamicAnalysis]':
        '''List[BearingDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5924.BearingDynamicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundDynamicAnalysis]':
        '''List[BearingCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5924.BearingDynamicAnalysis]':
        '''List[BearingDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5924.BearingDynamicAnalysis))
        return value

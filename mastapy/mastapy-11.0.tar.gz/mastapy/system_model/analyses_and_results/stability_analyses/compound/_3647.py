'''_3647.py

PointLoadCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2148
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3516
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3683
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'PointLoadCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundStabilityAnalysis',)


class PointLoadCompoundStabilityAnalysis(_3683.VirtualComponentCompoundStabilityAnalysis):
    '''PointLoadCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2148.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2148.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3516.PointLoadStabilityAnalysis]':
        '''List[PointLoadStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3516.PointLoadStabilityAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3516.PointLoadStabilityAnalysis]':
        '''List[PointLoadStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3516.PointLoadStabilityAnalysis))
        return value
